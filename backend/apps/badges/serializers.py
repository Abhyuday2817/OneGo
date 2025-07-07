from rest_framework import serializers
from .models import Badge, UserBadge
from apps.users.serializers import UserSerializer


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = [
            'id',
            'slug',
            'name',
            'description',
            'icon_url',
            'level',
            'expires_in_days',
        ]
        read_only_fields = ['id', 'slug']


class SimpleBadgeSerializer(serializers.ModelSerializer):
    """Used for nested user badge listing"""
    class Meta:
        model = Badge
        fields = ['id', 'name', 'icon_url']


class UserBadgeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    badge = SimpleBadgeSerializer(read_only=True)
    awarded_date = serializers.DateTimeField(source='awarded_at', read_only=True)
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = UserBadge
        fields = [
            'id',
            'user',
            'badge',
            'awarded_date',
            'verified',
            'expires_at',
            'note',
            'is_active',
        ]
        read_only_fields = ['id', 'awarded_date', 'is_active']

    def get_is_active(self, obj):
        return obj.is_active()


class AssignUserBadgeSerializer(serializers.ModelSerializer):
    """
    Assign a badge to a user.
    Accepts user_id and badge_id.
    """
    class Meta:
        model = UserBadge
        fields = ['user', 'badge', 'note']

    def validate(self, attrs):
        user = attrs.get("user")
        badge = attrs.get("badge")
        if UserBadge.objects.filter(user=user, badge=badge).exists():
            raise serializers.ValidationError("This user already has this badge.")
        return attrs


class VerifyBadgeSerializer(serializers.ModelSerializer):
    """
    Admin can verify a user's badge manually.
    """
    class Meta:
        model = UserBadge
        fields = ['verified']
