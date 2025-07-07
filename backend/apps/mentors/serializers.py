from rest_framework import serializers
from django.utils import timezone
from apps.mentors.models import MentorProfile, AvailabilityWindow, MentorAvailability
from apps.users.serializers import UserSerializer
from apps.categories.serializers import CategorySerializer
from apps.categories.models import Category

class AvailabilityWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityWindow
        fields = ['id', 'start', 'end', 'is_booked', 'created_at']
        read_only_fields = ['id', 'is_booked', 'created_at']

    def validate(self, data):
        # Use get for partial updates (PATCH)
        start = data.get('start', getattr(self.instance, 'start', None))
        end = data.get('end', getattr(self.instance, 'end', None))
        if start and end:
            if start >= end:
                raise serializers.ValidationError("Start time must be before end time")
            if start <= timezone.now():
                raise serializers.ValidationError("Availability cannot be in the past")
        return data

class MentorAvailabilitySerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = MentorAvailability
        fields = [
            'id', 'mentor', 'day', 'day_display', 'start_time', 'end_time',
            'timezone', 'is_available'
        ]
        read_only_fields = ['id', 'day_display']
        extra_kwargs = {
            'mentor': {'required': False}
        }

    def validate(self, data):
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))
        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("Start time must be before end time")
        return data

class MentorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specialties = CategorySerializer(many=True, read_only=True)
    specialty_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Category.objects.all(),
        source='specialties'
    )
    availability_windows = AvailabilityWindowSerializer(many=True, read_only=True)
    weekly_availability = MentorAvailabilitySerializer(many=True, read_only=True)

    # Computed fields
    upcoming_session_count = serializers.SerializerMethodField()
    total_earnings = serializers.SerializerMethodField()
    average_session_duration = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    next_available_slot = serializers.SerializerMethodField()

    class Meta:
        model = MentorProfile
        fields = [
            'id', 'user', 'bio', 'expertise', 'specialties', 'specialty_ids',
            'hourly_rate', 'per_minute_rate', 'rating', 'num_reviews',
            'certifications', 'languages', 'country', 'profile_photo',
            'linkedin_url', 'youtube_url', 'education', 'experience',
            'is_active', 'is_verified', 'availability_windows', 'weekly_availability',
            'upcoming_session_count', 'total_earnings', 'average_session_duration', 
            'total_students', 'next_available_slot', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'user', 'rating', 'num_reviews', 'is_verified',
            'upcoming_session_count', 'total_earnings', 'average_session_duration', 
            'total_students', 'next_available_slot', 'created_at', 'updated_at',
        ]

    def get_upcoming_session_count(self, obj):
        try:
            return obj.get_upcoming_sessions().count()
        except Exception:
            return 0

    def get_total_earnings(self, obj):
        try:
            return float(obj.total_earnings())
        except Exception:
            return 0.0

    def get_average_session_duration(self, obj):
        try:
            duration = obj.average_session_duration()
            return round(duration, 2) if duration else 0
        except Exception:
            return 0

    def get_total_students(self, obj):
        try:
            return obj.total_students_taught()
        except Exception:
            return 0

    def get_next_available_slot(self, obj):
        try:
            next_slot = obj.availability_windows.filter(
                start__gt=timezone.now(),
                is_booked=False
            ).first()
            return AvailabilityWindowSerializer(next_slot).data if next_slot else None
        except Exception:
            return None

class MentorProfileListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing mentors"""
    user = UserSerializer(read_only=True)
    specialties = CategorySerializer(many=True, read_only=True)
    next_available_slot = serializers.SerializerMethodField()

    class Meta:
        model = MentorProfile
        fields = [
            'id', 'user', 'bio', 'expertise', 'specialties',
            'hourly_rate', 'per_minute_rate', 'rating', 'num_reviews',
            'languages', 'country', 'profile_photo', 'is_verified',
            'next_available_slot'
        ]

    def get_next_available_slot(self, obj):
        try:
            next_slot = obj.availability_windows.filter(
                start__gt=timezone.now(),
                is_booked=False
            ).first()
            return next_slot.start if next_slot else None
        except Exception:
            return None