from rest_framework import serializers
from .models import SupportTicket
from apps.users.serializers import UserSerializer  # Ensure this exists and imports cleanly


# 🔹 Main Read Serializer (for GET)
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
        read_only_fields = [
            'id',
            'user',
            'created_at',
            'updated_at',
            'closed_at'
        ]


# 🔹 Serializer for Creating a Ticket
class SupportTicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message', 'priority']


# 🔹 Serializer for Admin/Staff Updating Ticket Fields
class SupportTicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['status', 'priority', 'assigned_to', 'resolution']


# 🔹 Serializer for Changing Status Only
class SupportTicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['status']
