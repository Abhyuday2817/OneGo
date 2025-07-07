# apps/appointments/serializers.py

from rest_framework import serializers
from django.utils import timezone
from .models import Appointment
from apps.users.serializers import UserSerializer
from apps.mentors.serializers import MentorProfileSerializer
from django.core.exceptions import ValidationError as DjangoValidationError


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Detailed read-only serializer for listing appointments.
    """
    student = UserSerializer(read_only=True)
    mentor = MentorProfileSerializer(read_only=True)
    duration_minutes = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    is_upcoming = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'student', 'mentor',
            'start_time', 'end_time',
            'duration_minutes', 'status', 'status_display',
            'notes', 'is_upcoming',
            'created_at',
        ]
        read_only_fields = [
            'id', 'student', 'mentor',
            'status', 'status_display',
            'created_at'
        ]

    def get_duration_minutes(self, obj):
        try:
            return int((obj.end_time - obj.start_time).total_seconds() // 60)
        except Exception:
            return None

    def get_is_upcoming(self, obj):
        return obj.start_time > timezone.now()



class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['mentor', 'start_time', 'end_time', 'notes']

    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data

    def create(self, validated_data):
        instance = Appointment(**validated_data)
        try:
            instance.full_clean()
        except DjangoValidationError as e:
            # Convert Django ValidationError to DRF ValidationError
            raise serializers.ValidationError(e.message_dict)
        instance.save()
        return instance




class AppointmentUpdateStatusSerializer(serializers.ModelSerializer):
    """
    Only used by admin or mentor to update status via PATCH.
    """
    class Meta:
        model = Appointment
        fields = ['status']
