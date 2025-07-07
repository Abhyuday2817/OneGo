import django_filters
from django_filters import rest_framework as filters
from .models import Bid
from django.db.models import Q


class BidFilter(filters.FilterSet):
    status      = filters.ChoiceFilter(
        field_name="status",
        choices=Bid.STATUS_CHOICES,
        lookup_expr="iexact",
        help_text="Filter by bid status: Pending, Accepted, Rejected"
    )
    mentor      = filters.CharFilter(
        field_name="mentor__user__username",
        lookup_expr="icontains",
        help_text="Mentor's username (partial match allowed)"
    )
    student     = filters.CharFilter(
        field_name="gig_request__student__username",
        lookup_expr="icontains",
        help_text="Gig owner/student username"
    )
    gig_id      = filters.NumberFilter(
        field_name="gig_request__id",
        help_text="Filter bids on specific gig ID"
    )
    min_rate    = filters.NumberFilter(
        field_name="proposed_rate",
        lookup_expr="gte",
        help_text="Minimum proposed rate"
    )
    max_rate    = filters.NumberFilter(
        field_name="proposed_rate",
        lookup_expr="lte",
        help_text="Maximum proposed rate"
    )
    created_after  = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        help_text="Bids created after this datetime"
    )
    created_before = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        help_text="Bids created before this datetime"
    )

    ordering = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("proposed_rate", "proposed_rate"),
            ("status", "status"),
        ),
        field_labels={
            "created_at": "Created At",
            "proposed_rate": "Proposed Rate",
            "status": "Status",
        },
        help_text="Order by created date, rate, or status"
    )

    class Meta:
        model = Bid
        fields = [
            "status",
            "mentor",
            "student",
            "gig_id",
            "min_rate",
            "max_rate",
            "created_after",
            "created_before",
        ]
