# consultations/serializers.py

from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Consultation
from apps.mentors.serializers import MentorProfileSerializer
from apps.users.serializers import UserSerializer

class ConsultationSerializer(serializers.ModelSerializer):
    # Nested read‐only representations
    student       = UserSerializer(read_only=True)
    mentor        = MentorProfileSerializer(read_only=True)

    # Writable FK fields
    mentor_id     = serializers.PrimaryKeyRelatedField(
        queryset=MentorProfileSerializer().Meta.model.objects.all(),
        source='mentor',
        write_only=True
    )

    # Computed fields
    join_url      = serializers.SerializerMethodField()
    can_join      = serializers.SerializerMethodField()
    end_time      = serializers.DateTimeField(source='end_time', read_only=True)
    duration      = serializers.SerializerMethodField()

    class Meta:
        model = Consultation
        fields = [
            "id",
            "topic", "description",

            "student",       # full student object
            "mentor",        # full mentor profile
            "mentor_id",     # for creation

            "scheduled_time",
            "duration_mins", # as stored
            "duration",      # human‐readable proxy
            "end_time",      # computed

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
        """Return duration in minutes as integer."""
        return obj.duration_mins

    def get_can_join(self, obj):
        """Whether the requesting user is allowed to join now."""
        user = self.context["request"].user
        return obj.can_join(user)

    def get_join_url(self, obj):
        """
        A frontend deep‐link to the Twilio room,
        only if the user can join right now.
        """
        request = self.context.get("request")
        if not request or not obj.can_join(request.user) or not obj.twilio_room_sid:
            return None
        return (
            f"{request.scheme}://{request.get_host()}"
            f"/consultations/join/{obj.twilio_room_sid}/"
        )

    def validate_scheduled_time(self, value):
        """Ensure you can’t create in the past."""
        if value <= timezone.now():
            raise serializers.ValidationError("scheduled_time must be in the future.")
        return value

    def validate(self, data):
        """
        Cross‐field validation: scheduling conflicts,
        student ≠ mentor, etc. Delegate to model.clean().
        """
        # Temporarily instantiate to run clean()
        obj = Consultation(**{**data, **{"student": self.context["request"].user}})
        try:
            obj.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict or e.messages)
        return data

    def create(self, validated_data):
        """
        On create, set the student automatically
        to the current user.
        """
        validated_data["student"] = self.context["request"].user
        return super().create(validated_data)
