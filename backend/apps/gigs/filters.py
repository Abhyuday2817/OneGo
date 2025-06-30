import django_filters
from .models import GigRequest, Bid

class GigRequestFilter(django_filters.FilterSet):
    status         = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    student        = django_filters.CharFilter(field_name="student__username", lookup_expr="iexact")
    category       = django_filters.NumberFilter(field_name="category__id")
    deadline_before = django_filters.DateTimeFilter(field_name="bidding_deadline", lookup_expr="lte")
    deadline_after  = django_filters.DateTimeFilter(field_name="bidding_deadline", lookup_expr="gte")

    class Meta:
        model = GigRequest
        fields = ["status", "student", "category", "deadline_before", "deadline_after"]
