from rest_framework import serializers
from apps.mentors.models import MentorProfile, AvailabilityWindow
from apps.users.serializers import UserSerializer  # or UserShortSerializer if you have it
from apps.categories.serializers import CategorySerializer

# Availability Window Serializer
class AvailabilityWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityWindow
        fields = ['id', 'start', 'end']
        read_only_fields = ['id']


# Mentor Profile Serializer
class MentorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specialties = CategorySerializer(many=True, read_only=True)

    specialty_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=CategorySerializer.Meta.model.objects.all(),
        source='specialties'
    )

    upcoming_session_count = serializers.SerializerMethodField()
    total_earnings = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='total_earnings',
        read_only=True
    )

    class Meta:
        model = MentorProfile
        fields = [
            'id', 'user', 'bio', 'specialties', 'specialty_ids',
            'hourly_rate', 'per_minute_rate',
            'rating', 'num_reviews',
            'certifications', 'languages',
            'availability_windows',
            'upcoming_session_count',
            'total_earnings',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'user', 'rating', 'num_reviews', 'upcoming_session_count',
            'total_earnings', 'created_at', 'updated_at'
        ]

    def get_upcoming_session_count(self, obj):
        return obj.get_upcoming_sessions().count()

