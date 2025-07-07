from rest_framework import serializers
from .models import Bid
from apps.mentors.serializers import MentorProfileSerializer
from apps.users.serializers import UserSerializer


class BidSerializer(serializers.ModelSerializer):
    mentor = MentorProfileSerializer(read_only=True)
    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=MentorProfileSerializer.Meta.model.objects.all(),
        source="mentor",
        write_only=True
    )
    gig_request_id = serializers.PrimaryKeyRelatedField(
        queryset=Bid._meta.get_field("gig_request").related_model.objects.all(),
        source="gig_request",
        write_only=True
    )
    student_username = serializers.CharField(
        source="gig_request.student.username", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model = Bid
        fields = [
            "id",
            "gig_request", "gig_request_id",
            "student_username",
            "mentor", "mentor_id",
            "proposed_rate", "proposal_text",
            "status", "status_display",
            "created_at", "updated_at"
        ]
        read_only_fields = [
            "id", "gig_request", "mentor",
            "status", "status_display",
            "created_at", "updated_at",
            "student_username"
        ]

    def validate(self, data):
        """
        Ensure proposed rate is within the budget range of the gig request.
        """
        gig = data.get("gig_request") or getattr(self.instance, "gig_request", None)
        rate = data.get("proposed_rate") or getattr(self.instance, "proposed_rate", None)

        if not gig or not rate:
            raise serializers.ValidationError("Gig and proposed rate are required.")

        if rate < gig.budget_min or rate > gig.budget_max:
            raise serializers.ValidationError(
                f"Proposed rate must be between {gig.budget_min} and {gig.budget_max}."
            )

        return data

    def create(self, validated_data):
        bid = super().create(validated_data)

        # Notify student
        from services.notifications import notify_user
        notify_user(
            bid.gig_request.student,
            f"{bid.mentor.user.username} placed a new bid on your gig “{bid.gig_request.title}”."
        )

        return bid

    def update(self, instance, validated_data):
        """
        Optional: Custom logic when mentor edits bid (if allowed)
        """
        previous_rate = instance.proposed_rate
        instance = super().update(instance, validated_data)

        # Optional: notify student if rate or proposal updated
        if instance.proposed_rate != previous_rate:
            from services.notifications import notify_user
            notify_user(
                instance.gig_request.student,
                f"{instance.mentor.user.username} updated their bid on your gig “{instance.gig_request.title}”."
            )

        return instance
