import django_filters
from .models import Bid

class BidFilter(django_filters.FilterSet):
    status     = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    mentor     = django_filters.CharFilter(field_name="mentor__user__username", lookup_expr="iexact")
    gig        = django_filters.NumberFilter(field_name="gig_request__id")
    min_rate   = django_filters.NumberFilter(field_name="proposed_rate", lookup_expr="gte")
    max_rate   = django_filters.NumberFilter(field_name="proposed_rate", lookup_expr="lte")
    date_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    date_before= django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Bid
        fields = ["status", "mentor", "gig", "min_rate", "max_rate", "date_after", "date_before"]
