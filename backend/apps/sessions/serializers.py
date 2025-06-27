from rest_framework import serializers
from django.utils import timezone
from .models import Session
from apps.users.serializers import UserSerializer
from apps.mentors.serializers import MentorProfileSerializer
from services.availability import is_available

class SessionSerializer(serializers.ModelSerializer):
    student        = UserSerializer(read_only=True)
    student_id     = serializers.PrimaryKeyRelatedField(
                         queryset=UserSerializer().Meta.model.objects.all(),
                         write_only=True, source="student"
                     )
    mentor         = MentorProfileSerializer(read_only=True)
    mentor_id      = serializers.PrimaryKeyRelatedField(
                         queryset=MentorProfileSerializer().Meta.model.objects.all(),
                         write_only=True, source="mentor"
                     )
    duration       = serializers.IntegerField(source="duration_minutes", read_only=True)
    total_cost     = serializers.FloatField(source="total_cost", read_only=True)
    can_cancel     = serializers.SerializerMethodField()
    can_confirm    = serializers.BooleanField(read_only=True, default=True)

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
            "created_at",
        ]
        read_only_fields = [
            "id", "verified", "duration", "total_cost",
            "status", "created_at", "can_cancel", "can_confirm"
        ]

    def get_can_cancel(self, obj):
        # only scheduled sessions > 1h before start can be cancelled
        return (
            obj.status == Session.STATUS_SCHEDULED and
            (obj.start_time - timezone.now()).total_seconds() > 3600
        )

    def validate(self, data):
        # ensure availability
        start = data.get("start_time", getattr(self.instance, "start_time", None))
        end   = data.get("end_time",   getattr(self.instance, "end_time", None))
        mentor = data.get("mentor", getattr(self.instance, "mentor", None))
        if start and end and mentor and not is_available(mentor, start, end):
            raise serializers.ValidationError("Mentor is not available in that time slot.")
        return data
