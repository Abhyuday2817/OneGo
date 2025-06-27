from django.db.models import Sum
from rest_framework import serializers
from apps.wallets.models import Wallet
from apps.transactions.serializers import TransactionSerializer

class WalletSerializer(serializers.ModelSerializer):
    user_username       = serializers.CharField(source="user.username", read_only=True)
    total_deposits      = serializers.SerializerMethodField()
    total_withdrawals   = serializers.SerializerMethodField()
    recent_transactions = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = [
            "id",
            "user",
            "user_username",
            "balance",
            "escrowed",
            "total_deposits",
            "total_withdrawals",
            "recent_transactions",
        ]
        read_only_fields = [
            "balance",
            "escrowed",
            "total_deposits",
            "total_withdrawals",
            "recent_transactions",
        ]

    def get_total_deposits(self, obj):
        agg = obj.user.transactions.filter(txn_type="deposit").aggregate(sum=Sum("amount"))
        return agg["sum"] or 0

    def get_total_withdrawals(self, obj):
        agg = obj.user.transactions.filter(txn_type="withdraw").aggregate(sum=Sum("amount"))
        # amount field for withdrawals is negative in our logs, so invert
        return -(agg["sum"] or 0)

    def get_recent_transactions(self, obj):
        qs = obj.user.transactions.all().order_by("-timestamp")[:5]
        return TransactionSerializer(qs, many=True, context=self.context).data
