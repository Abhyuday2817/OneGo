# payments/views.py

from decimal import Decimal
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.http import HttpResponse
from apps.payments.models import Payment
from apps.payments.services.invoice import render_invoice_pdf
from rest_framework import viewsets, mixins, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet, Transaction, Payment
from .serializers import (
    WalletSerializer,
    TransactionSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
)
from .services.invoice import render_invoice_pdf  # your PDF generator


# ──────────────────────────────────────────────────────────────────────────────
# Wallet & Transactions
# ──────────────────────────────────────────────────────────────────────────────

class WalletViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin):
    """
    list /api/payments/wallets/             → all wallets (admin-only)
    retrieve /api/payments/wallets/{pk}/    → single wallet by ID
    top_up /api/payments/wallets/{pk}/top_up/    [POST]  +amount
    hold   /api/payments/wallets/{pk}/hold/      [POST]  +amount, ref
    release/api/payments/wallets/{pk}/release/   [POST]  +amount, ref
    """
    queryset = Wallet.objects.select_related("user").all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # normal users only see their own wallet
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    @action(detail=True, methods=["post"])
    def top_up(self, request, pk=None):
        wallet = self.get_object()
        amt = Decimal(request.data.get("amount", 0))
        wallet.deposit(amt, reference=f"topup-{request.user.id}")
        return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def hold(self, request, pk=None):
        wallet = self.get_object()
        amt = Decimal(request.data.get("amount", 0))
        wallet.hold_in_escrow(amt, reference=request.data.get("ref", ""))
        return Response({
            "balance": wallet.balance,
            "escrowed": wallet.escrowed
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def release(self, request, pk=None):
        wallet = self.get_object()
        amt = Decimal(request.data.get("amount", 0))
        wallet.release_escrow(amt, reference=request.data.get("ref", ""))
        return Response({
            "balance": wallet.balance,
            "escrowed": wallet.escrowed
        }, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list /api/payments/transactions/       → all ledger entries
    retrieve /api/payments/transactions/{pk}/
    """
    queryset = Transaction.objects.select_related("user").all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["timestamp", "amount"]
    ordering = ["-timestamp"]

    def get_queryset(self):
        # users only see their own transactions unless staff
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


# ──────────────────────────────────────────────────────────────────────────────
# Payments & Checkout
# ──────────────────────────────────────────────────────────────────────────────

class PaymentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin):
    """
    list    GET    /api/payments/payments/
    retrieveGET    /api/payments/payments/{pk}/
    create  POST   /api/payments/payments/            → uses PaymentCreateSerializer
    update  PATCH  /api/payments/payments/{pk}/
    refund  POST   /api/payments/payments/{pk}/refund/
    invoice GET    /api/payments/payments/{pk}/invoice/
    stats   GET    /api/payments/payments/stats/?period=day|month
    webhook POST   /api/payments/payments/webhook/
    """
    queryset = Payment.objects.select_related("user").all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "amount"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer

    def get_queryset(self):
        # users only see their own payments unless staff
        qs = self.queryset
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        payment = self.get_object()
        if not payment.is_successful():
            return Response(
                {"detail": "Only completed payments can be refunded."},
                status=status.HTTP_400_BAD_REQUEST
            )
        payment.refund(reference=f"refund-{payment.pk}")
        return Response({"status": "refunded"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def invoice(self, request, pk=None):
        payment = self.get_object()
        pdf_bytes = render_invoice_pdf(payment)
        return Response(pdf_bytes, content_type="application/pdf")

    @action(detail=False, methods=["get"])
    def stats(self, request):
        period = request.query_params.get("period", "month")
        qs = Payment.objects.filter(
            user=request.user,
            status=Payment.STATUS_COMPLETED
        )
        if period == "day":
            today = timezone.now().date()
            qs = qs.filter(created_at__date=today)
        total = qs.aggregate(Sum("amount"))["amount__sum"] or Decimal("0.00")
        return Response({"period": period, "total_paid": total})

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=["post"], url_path="webhook")
    def webhook(self, request):
        # TODO: validate signature, then update payment.status accordingly
        return Response(status=status.HTTP_200_OK)


# ──────────────────────────────────────────────────────────────────────────────
# Legacy checkout/result for compatibility
# ──────────────────────────────────────────────────────────────────────────────

class CheckoutView(APIView):
    """
    POST /api/payments/checkout/
      { "amount": 100.0, "method": "stripe", "metadata": {...} }
    Creates a Payment (pending) and returns its ID+status.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        payment = Payment.objects.create(
            user=request.user,
            amount=request.data.get("amount"),
            method=request.data.get("method", ""),
            transaction_id=request.data.get("transaction_id", ""),
            metadata=request.data.get("metadata", {})
        )
        return Response(
            {"payment_id": payment.id, "status": payment.status},
            status=status.HTTP_201_CREATED
        )


class PaymentResultView(APIView):
    """
    GET /api/payments/result/?payment_id=123
    Returns the details of that payment.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pid = request.query_params.get("payment_id")
        payment = Payment.objects.filter(id=pid, user=request.user).first()
        if not payment:
            return Response(
                {"error": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(PaymentSerializer(payment).data)




def test_invoice_pdf(request):
    payment = Payment.objects.first()
    pdf_data = render_invoice_pdf(payment)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response
