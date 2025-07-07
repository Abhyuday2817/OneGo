from rest_framework import serializers
from .models import Notification
from apps.users.serializers import UserSerializer  # Assumes this exists for frontend user display

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # For admin or frontend to display sender info
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    is_expired = serializers.SerializerMethodField()
    created_at_formatted = serializers.DateTimeField(source="created_at", format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "message",
            "link",
            "unread",
            "priority",
            "priority_display",
            "type",
            "type_display",
            "is_archived",
            "expires_at",
            "created_at",
            "created_at_formatted",
            "is_expired"
        ]
        read_only_fields = [
            "id", "user", "created_at", "created_at_formatted",
            "priority_display", "type_display", "is_expired"
        ]

    def get_is_expired(self, obj):
        return obj.is_expired()
