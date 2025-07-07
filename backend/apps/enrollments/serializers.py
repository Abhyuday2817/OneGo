from rest_framework import serializers
from .models import Enrollment
from apps.users.serializers import UserSerializer
from apps.courses.serializers import CourseSerializer
from django.contrib.auth import get_user_model
from apps.courses.models import Course

User = get_user_model()

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="student",
        write_only=True
    )

    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source="course",
        write_only=True
    )

    progress_pct = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    modules_remaining = serializers.SerializerMethodField()
    days_since_enroll = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            "id", "student", "student_id",
            "course", "course_id",
            "enrolled_at", "completed", "progress",
            "progress_pct", "time_since",
            "modules_remaining", "days_since_enroll", "is_active"
        ]
        read_only_fields = [
            "id", "enrolled_at", "progress_pct", "time_since",
            "modules_remaining", "days_since_enroll", "is_active"
        ]

    # ─── Computed Properties ──────────────────────────────
    def get_progress_pct(self, obj):
        return obj.progress_percent

    def get_time_since(self, obj):
        delta = obj.time_since_enroll()
        return f"{delta.days}d {delta.seconds // 3600}h"

    def get_modules_remaining(self, obj):
        return obj.modules_remaining

    def get_days_since_enroll(self, obj):
        return obj.days_since_enrollment

    def get_is_active(self, obj):
        return obj.is_active

    # ─── Validation & Creation ─────────────────────────────
    def validate(self, data):
        student = data.get("student", getattr(self.instance, "student", None))
        course = data.get("course", getattr(self.instance, "course", None))

        if self.instance is None and student and course:
            if Enrollment.objects.filter(student=student, course=course).exists():
                raise serializers.ValidationError("Student is already enrolled in this course.")
        return data

    def create(self, validated_data):
        # Auto-fill student if not explicitly passed (e.g. via view logic)
        if "student" not in validated_data:
            validated_data["student"] = self.context["request"].user
        return super().create(validated_data)
