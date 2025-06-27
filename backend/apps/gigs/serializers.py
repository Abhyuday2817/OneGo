from rest_framework import serializers
from django.utils import timezone
from .models import GigRequest, Bid, Contract
from apps.categories.serializers import CategorySerializer
from apps.mentors.serializers import MentorProfileSerializer
from apps.users.serializers import UserSerializer

class BidSerializer(serializers.ModelSerializer):
    mentor          = MentorProfileSerializer(read_only=True)
    mentor_id       = serializers.PrimaryKeyRelatedField(
        queryset=MentorProfileSerializer().Meta.model.objects.all(),
        source="mentor",
        write_only=True
    )
    status_display  = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Bid
        fields = [
            "id", "gig_request", "mentor", "mentor_id",
            "proposed_rate", "proposal_text",
            "status", "status_display",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]


class ContractSerializer(serializers.ModelSerializer):
    bid         = BidSerializer(read_only=True)
    bid_id      = serializers.PrimaryKeyRelatedField(
        queryset=Bid.objects.filter(status=Bid.STATUS_ACCEPTED),
        source="bid",
        write_only=True
    )
    student     = UserSerializer(read_only=True)
    mentor      = MentorProfileSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Contract
        fields = [
            "id", "bid", "bid_id",
            "student", "mentor",
            "start_date", "end_date",
            "status", "status_display"
        ]
        read_only_fields = ["id", "start_date", "status", "status_display"]


class GigRequestSerializer(serializers.ModelSerializer):
    student         = UserSerializer(read_only=True)
    student_id      = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer().Meta.model.objects.all(),
        source="student",
        write_only=True
    )
    category        = CategorySerializer(read_only=True)
    category_id     = serializers.PrimaryKeyRelatedField(
        queryset=CategorySerializer().Meta.model.objects.all(),
        source="category",
        write_only=True
    )
    bids            = BidSerializer(many=True, read_only=True)
    bid_count       = serializers.IntegerField(source="bids.count", read_only=True)
    contracts       = ContractSerializer(many=True, read_only=True)
    contract_count  = serializers.IntegerField(source="contracts.count", read_only=True)
    is_open         = serializers.BooleanField(source="is_open", read_only=True)

    class Meta:
        model = GigRequest
        fields = [
            "id", "student", "student_id",
            "category", "category_id",
            "title", "description",
            "budget_min", "budget_max",
            "bidding_deadline", "status",
            "created_at", "updated_at",
            "bids", "bid_count",
            "contracts", "contract_count",
            "is_open"
        ]
        read_only_fields = [
            "id", "status", "created_at", "updated_at",
            "bids", "bid_count", "contracts", "contract_count", "is_open"
        ]

    def validate(self, data):
        # ensure budgets make sense
        if data["budget_max"] < data["budget_min"]:
            raise serializers.ValidationError("budget_max must be >= budget_min")
        if data["bidding_deadline"] <= timezone.now():
            raise serializers.ValidationError("bidding_deadline must be in the future")
        return data
