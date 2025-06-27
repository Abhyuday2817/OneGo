from rest_framework import serializers
from .models import Enrollment
from apps.users.serializers import UserSerializer
from apps.courses.serializers import CourseSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student         = UserSerializer(read_only=True)
    student_id      = serializers.PrimaryKeyRelatedField(
                          queryset=UserSerializer().Meta.model.objects.all(),
                          source="student",
                          write_only=True
                      )
    course          = CourseSerializer(read_only=True)
    course_id       = serializers.PrimaryKeyRelatedField(
                          queryset=CourseSerializer().Meta.model.objects.all(),
                          source="course",
                          write_only=True
                      )
    progress_pct    = serializers.SerializerMethodField()
    time_since      = serializers.SerializerMethodField()
    modules_remaining = serializers.SerializerMethodField()
    days_since_enroll = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            "id", "student", "student_id", "course", "course_id",
            "enrolled_at", "completed", "progress",
            "progress_pct", "time_since", "modules_remaining", "days_since_enroll"
        ]
        read_only_fields = [
            "id", "enrolled_at", "progress_pct", "time_since",
            "modules_remaining", "days_since_enroll"
        ]

    def get_progress_pct(self, obj):
        return obj.progress_percent

    def get_time_since(self, obj):
        delta = obj.time_since_enroll()
        days = delta.days
        hours = delta.seconds // 3600
        return f"P{days}DT{hours}H"

    def get_modules_remaining(self, obj):
        return obj.modules_remaining

    def get_days_since_enroll(self, obj):
        return obj.days_since_enrollment

    def validate(self, data):
        student = data.get("student", getattr(self.instance, "student", None))
        course  = data.get("course", getattr(self.instance, "course", None))
        if self.instance is None and Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Enrollment already exists.")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["student"] = user
        return super().create(validated_data)