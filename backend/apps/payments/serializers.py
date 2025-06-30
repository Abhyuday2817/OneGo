from rest_framework import serializers
from .models import Wallet, Transaction, Payment
from apps.users.serializers import UserSerializer

class TransactionSerializer(serializers.ModelSerializer):
    user       = UserSerializer(read_only=True)
    balance_after = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            "id", "user", "txn_type", "amount",
            "reference", "metadata",
            "timestamp", "balance_after"
        ]
        read_only_fields = ["id","timestamp","balance_after"]

    def to_representation(self, inst):
        data = super().to_representation(inst)
        # compute balance after by summing
        qs = Transaction.objects.filter(
            user=inst.user,
            timestamp__lte=inst.timestamp
        )
        data["balance_after"] = sum(t.amount for t in qs)
        return data

class WalletSerializer(serializers.ModelSerializer):
    user         = UserSerializer(read_only=True)
    balance      = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    escrowed     = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ["user","balance","escrowed","transactions"]

class PaymentSerializer(serializers.ModelSerializer):
    user           = UserSerializer(read_only=True)
    is_successful  = serializers.BooleanField(source="is_successful", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id", "user", "amount", "currency",
            "status", "method", "transaction_id",
            "metadata", "created_at","updated_at",
            "is_successful"
        ]
        read_only_fields = ["id","status","transaction_id","is_successful","created_at","updated_at"]

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["amount","currency","method","metadata"]

    def validate_amount(self, v):
        if v <= 0:
            raise serializers.ValidationError("Must be positive.")
        return v

    def create(self, data):
        user = self.context["request"].user
        payment = Payment.objects.create(user=user, **data)
        # e.g. call Stripe/Razorpay here, store transaction_id
        return payment
