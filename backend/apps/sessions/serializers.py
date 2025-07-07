from rest_framework import serializers
from django.utils import timezone
from .models import Session
from apps.users.serializers import UserSerializer
from apps.mentors.serializers import MentorProfileSerializer
from services.availability import is_available


class SessionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer().Meta.model.objects.all(),
        write_only=True,
        source="student"
    )
    mentor = MentorProfileSerializer(read_only=True)
    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=MentorProfileSerializer().Meta.model.objects.all(),
        write_only=True,
        source="mentor"
    )

    duration = serializers.IntegerField(source="duration_minutes", read_only=True)
    total_cost = serializers.FloatField(source="total_cost", read_only=True)
    can_cancel = serializers.SerializerMethodField()
    can_confirm = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = Session
        fields = [
            "id", "student", "student_id",
            "mentor", "mentor_id",
            "start_time", "end_time",
            "session_type", "rate_applied",
            "status", "verified",
            "duration", "total_cost",
            "can_cancel", "can_confirm",
            "created_at"
        ]
        read_only_fields = [
            "id", "status", "verified", "duration", "total_cost",
            "can_cancel", "can_confirm", "created_at"
        ]

    def get_can_cancel(self, obj):
        if obj.status != Session.STATUS_SCHEDULED:
            return False
        time_diff = (obj.start_time - timezone.now()).total_seconds()
        return time_diff > 3600  # Only cancel if more than 1 hour left

    def validate(self, data):
        start = data.get("start_time", getattr(self.instance, "start_time", None))
        end = data.get("end_time", getattr(self.instance, "end_time", None))
        mentor = data.get("mentor", getattr(self.instance, "mentor", None))

        if start and end and mentor and not is_available(mentor, start, end):
            raise serializers.ValidationError("Mentor is not available in that time slot.")

        if start and end and start >= end:
            raise serializers.ValidationError("End time must be after start time.")

        return data


class SessionStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["status"]


class SessionVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["student_confirmed", "mentor_confirmed"]


class SessionTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["actual_start_time", "actual_end_time", "duration_minutes", "total_price"]
        read_only_fields = fields
