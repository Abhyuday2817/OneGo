from rest_framework import serializers
from .models import SupportTicket
from apps.users.serializers import UserSerializer  # Make sure this file and class exist

class SupportTicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            'id',
            'user',
            'subject',
            'message',
            'status',
            'priority',
            'assigned_to',
            'resolution',
            'created_at',
            'updated_at',
            'closed_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at']
