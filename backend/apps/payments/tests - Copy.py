from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer)
    user_username = serializers.CharField(source='user.username', read_only=True)
    class Meta
        model = Payment
        fields = ['id', 'user', 'user_username', 'amount', 'status', 'created_at', 'transaction_id', 'method']
        read_only_fields = ['created_at', 'user_username', 'transaction_id']