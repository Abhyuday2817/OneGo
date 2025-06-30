from rest_framework import viewsets, mixins, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Wallet
from .serializers import WalletSerializer
from apps.transactions.serializers import TransactionSerializer

class WalletViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    retrieve: Fetch a single wallet by username (staff/all users).
    list:     Admin-only full wallet list.
    Actions:
      - top_up
      - withdraw
      - hold
      - release
      - transactions (filterable)
    """
    queryset = Wallet.objects.select_related("user").all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "user__username"

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["user__username"]
    ordering_fields = ["balance", "escrowed"]
    ordering = ["-balance"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def _safe_amount(self, request):
        try:
            return float(request.data.get("amount", 0))
        except Exception:
            raise ValueError("Amount must be a valid number.")

    def _handle_wallet_action(self, wallet, method, request):
        ref = request.data.get("reference", "")
        try:
            amount = self._safe_amount(request)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            getattr(wallet, method)(amount, reference=ref)
            return Response(self.get_serializer(wallet).data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def top_up(self, request, user__username=None):
        return self._handle_wallet_action(self.get_object(), "deposit", request)

    @action(detail=True, methods=["post"])
    def withdraw(self, request, user__username=None):
        return self._handle_wallet_action(self.get_object(), "withdraw", request)

    @action(detail=True, methods=["post"])
    def hold(self, request, user__username=None):
        return self._handle_wallet_action(self.get_object(), "hold_in_escrow", request)

    @action(detail=True, methods=["post"])
    def release(self, request, user__username=None):
        return self._handle_wallet_action(self.get_object(), "release_escrow", request)

    @action(detail=True, methods=["get"])
    def transactions(self, request, user__username=None):
        """
        GET /api/wallets/{username}/transactions/?type=&after=
        Optional query params:
            - type: deposit / withdraw / escrow_hold / escrow_release
            - after: ISO date filter
        """
        wallet = self.get_object()
        tx_qs = wallet.transactions.all()
        ttype = request.query_params.get("type")
        after = request.query_params.get("after")

        if ttype:
            tx_qs = tx_qs.filter(txn_type=ttype)
        if after:
            tx_qs = tx_qs.filter(timestamp__gte=after)

        page = self.paginate_queryset(tx_qs)
        serializer = TransactionSerializer(page or tx_qs, many=True, context={"request": request})

        return (
            self.get_paginated_response(serializer.data)
            if page is not None else
            Response(serializer.data)
        )
