# apps/appointments/serializers.py

from rest_framework import serializers
from .models import Appointment
from apps.users.serializers import UserSerializer
from apps.mentors.serializers import MentorProfileSerializer  # Adjust if renamed

class AppointmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    mentor = MentorProfileSerializer(read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'student', 'mentor', 'scheduled_time', 'duration',
            'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def get_duration(self, obj):
        try:
            return obj.duration().total_seconds() // 60
        except Exception:
            return None


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['mentor', 'scheduled_time', 'duration']
