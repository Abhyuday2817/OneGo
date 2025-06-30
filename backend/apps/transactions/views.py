from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list / retrieve transaction logs

    Custom Actions:
    - GET /transactions/summary/?start=YYYY-MM-DD&end=YYYY-MM-DD
      → Aggregated totals for credits, debits, and count by type.
    """
    serializer_class = TransactionSerializer
    permission_classes = []  # You can customize as needed
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["timestamp", "amount"]
    ordering = ["-timestamp"]
    search_fields = ["reference", "txn_type"]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.for_user(user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """
        GET /transactions/summary/?start=YYYY-MM-DD&end=YYYY-MM-DD
        """
        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")

        try:
            start = timezone.datetime.fromisoformat(start_str).replace(tzinfo=timezone.utc) if start_str else timezone.now().replace(hour=0, minute=0, second=0)
            end = timezone.datetime.fromisoformat(end_str).replace(tzinfo=timezone.utc) if end_str else timezone.now()
        except Exception:
            return Response(
                {"detail": "Invalid date format; use ISO 8601 like YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )

        qs = self.get_queryset().in_period(start, end)

        credits = qs.filter(txn_type__in=[Transaction.TYPE_DEPOSIT, Transaction.TYPE_ESCROW_RELEASE]).aggregate(
            total=Sum("amount")
        )["total"] or 0

        debits = qs.filter(txn_type__in=[Transaction.TYPE_WITHDRAW, Transaction.TYPE_ESCROW_HOLD]).aggregate(
            total=Sum("amount")
        )["total"] or 0

        breakdown = qs.values("txn_type").annotate(
            count=Count("id"),
            sum=Sum("amount")
        )

        return Response({
            "period": {
                "start": start.strftime('%Y-%m-%d %H:%M'),
                "end": end.strftime('%Y-%m-%d %H:%M'),
            },
            "total_credits": credits,
            "total_debits": debits,
            "breakdown": breakdown,
        })
