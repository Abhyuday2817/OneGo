# transactions/serializers.py
from decimal import Decimal
from django.db.models import Sum
from rest_framework import serializers
from .models import Transaction
from apps.wallets.models import Wallet  # ✅ correct import

class TransactionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_credit     = serializers.SerializerMethodField()
    is_debit      = serializers.SerializerMethodField()
    balance_after = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        help_text="Wallet balance immediately after this transaction"
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user", "user_username",
            "amount",
            "txn_type",
            "is_credit", "is_debit",
            "timestamp",
            "reference",
            "metadata",
            "balance_after",
        ]
        read_only_fields = [
            "id", "user_username", "timestamp",
            "is_credit", "is_debit", "balance_after"
        ]

    def get_is_credit(self, obj):
        return obj.is_credit

    def get_is_debit(self, obj):
        return obj.is_debit

    def to_representation(self, instance):
        """
        Override to inject `balance_after` by summing all past transactions.
        """
        data = super().to_representation(instance)

        # Sum up to and including this transaction
        total = (
            Transaction.objects
            .filter(user=instance.user, timestamp__lte=instance.timestamp)
            .aggregate(sum=Sum('amount'))['sum']
            or Decimal('0.00')
        )
        data['balance_after'] = f"{total:.2f}"
        return data


class TransactionCreateSerializer(serializers.ModelSerializer):
    """
    Used for POST /transactions/ to deposit/withdraw funds.
    """
    class Meta:
        model = Transaction
        fields = ['amount', 'txn_type', 'reference', 'metadata']

    def validate_txn_type(self, value):
        if value not in (Transaction.TYPE_DEPOSIT, Transaction.TYPE_WITHDRAW):
            raise serializers.ValidationError("txn_type must be 'deposit' or 'withdraw'.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be strictly positive.")
        return value

    def create(self, validated_data):
        """
        Route through Wallet methods so that balance updates and ledger entries
        are always consistent.
        """
        user = self.context['request'].user
        wallet, _ = Wallet.objects.get_or_create(user=user)

        amount = validated_data['amount']
        txn_type = validated_data['txn_type']
        reference = validated_data.get('reference', '')
        metadata = validated_data.get('metadata', {})

        # Perform action on the wallet, which will create the Transaction record
        if txn_type == Transaction.TYPE_DEPOSIT:
            wallet.deposit(amount, reference=reference)
        else:  # withdraw
            wallet.withdraw(amount, reference=reference)

        # Grab the last transaction for this user
        return (
            Transaction.objects
            .filter(user=user)
            .order_by('-timestamp')
            .first()
        )
