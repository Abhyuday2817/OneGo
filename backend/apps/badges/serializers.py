from rest_framework import serializers
from .models import Badge, UserBadge
from apps.users.serializers import UserSerializer

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'icon']
        read_only_fields = ['id']

class UserBadgeSerializer(serializers.ModelSerializer):
    user          = UserSerializer(read_only=True)
    badge         = BadgeSerializer(read_only=True)
    awarded_date  = serializers.DateTimeField(source='awarded_at', read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'user', 'badge', 'awarded_date']
        read_only_fields = ['id', 'awarded_date']
