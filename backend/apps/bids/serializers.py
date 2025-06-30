from rest_framework import serializers
from .models import Bid
from apps.mentors.serializers import MentorProfileSerializer
from apps.users.serializers import UserSerializer

class BidSerializer(serializers.ModelSerializer):
    mentor          = MentorProfileSerializer(read_only=True)
    mentor_id       = serializers.PrimaryKeyRelatedField(
        queryset=MentorProfileSerializer().Meta.model.objects.all(),
        source="mentor",
        write_only=True
    )
    gig_request_id  = serializers.PrimaryKeyRelatedField(
        queryset=Bid._meta.get_field("gig_request").related_model.objects.all(),
        source="gig_request",
        write_only=True
    )
    student_username = serializers.CharField(
        source="gig_request.student.username", read_only=True
    )
    status_display   = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model = Bid
        fields = [
            "id", "gig_request", "gig_request_id",
            "student_username",
            "mentor", "mentor_id",
            "proposed_rate", "proposal_text",
            "status", "status_display",
            "created_at", "updated_at"
        ]
        read_only_fields = [
            "id", "status", "created_at", "updated_at",
            "student_username", "status_display"
        ]

    def validate(self, data):
        # ensure bid rate in bounds
        gig = data.get("gig_request") or self.instance.gig_request
        rate = data.get("proposed_rate") or self.instance.proposed_rate
        if not (gig.budget_min <= rate <= gig.budget_max):
            raise serializers.ValidationError(
                f"Rate must be between {gig.budget_min} and {gig.budget_max}"
            )
        return super().validate(data)

    def create(self, validated_data):
        bid = super().create(validated_data)
        # notify student
        from services.notifications import notify_user
        notify_user(
            bid.gig_request.student,
            f"{bid.mentor.user.username} placed a new bid on your gig “{bid.gig_request.title}”."
        )
        return bid
