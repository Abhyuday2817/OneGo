from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Consultation
from apps.mentors.serializers import MentorProfileSerializer
from apps.users.serializers import UserSerializer


class ConsultationSerializer(serializers.ModelSerializer):
    # ✅ Nested representations
    student = UserSerializer(read_only=True)
    mentor = MentorProfileSerializer(read_only=True)

    # ✅ Write-only field to pass mentor_id
    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=MentorProfileSerializer.Meta.model.objects.all(),
        source="mentor",
        write_only=True
    )

    # ✅ Computed fields
    join_url = serializers.SerializerMethodField()
    can_join = serializers.SerializerMethodField()
    end_time = serializers.DateTimeField(read_only=True)  # ✅ Fixed redundant source
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Consultation
        fields = [
            "id",
            "topic",
            "description",
            "student",
            "mentor",
            "mentor_id",
            "scheduled_time",
            "duration_mins",
            "duration",
            "end_time",
            "status",
            "twilio_room_sid",
            "can_join",
            "join_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "student",
            "mentor",
            "status",
            "twilio_room_sid",
            "end_time",
            "duration",
            "can_join",
            "join_url",
            "created_at",
            "updated_at",
        ]

    def get_duration(self, obj):
        """Returns a readable format like '45 mins'."""
        return f"{obj.duration_mins} mins"

    def get_can_join(self, obj):
        """Whether the current user can join the call."""
        request = self.context.get("request")
        return obj.can_join(request.user) if request else False

    def get_join_url(self, obj):
        """Constructs the join URL if user is eligible."""
        request = self.context.get("request")
        if not request or not obj.can_join(request.user) or not obj.twilio_room_sid:
            return None
        return f"{request.scheme}://{request.get_host()}/consultations/join/{obj.twilio_room_sid}/"

    def validate_scheduled_time(self, value):
        """Prevent booking in the past."""
        if value <= timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future.")
        return value

    def validate(self, data):
        """Run model-level clean() to catch conflicts."""
        temp_obj = Consultation(
            **data, student=self.context["request"].user
        )
        try:
            temp_obj.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict or e.messages)
        return data

    def create(self, validated_data):
        """Assign student from request context."""
        validated_data["student"] = self.context["request"].user
        return super().create(validated_data)
