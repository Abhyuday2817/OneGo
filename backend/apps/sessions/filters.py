from django_filters import rest_framework as df_filters
from django.utils import timezone
from .models import Session

class SessionFilter(df_filters.FilterSet):
    student      = df_filters.NumberFilter(field_name="student_id")
    mentor       = df_filters.NumberFilter(field_name="mentor_id")
    status       = df_filters.CharFilter(field_name="status")
    session_type = df_filters.CharFilter(field_name="session_type")
    date_from    = df_filters.DateTimeFilter(field_name="start_time", lookup_expr="gte")
    date_to      = df_filters.DateTimeFilter(field_name="end_time",   lookup_expr="lte")
    min_cost     = df_filters.NumberFilter(method="filter_min_cost")
    max_cost     = df_filters.NumberFilter(method="filter_max_cost")

    class Meta:
        model = Session
        fields = [
            "student", "mentor", "status",
            "session_type", "date_from", "date_to",
            "min_cost", "max_cost",
        ]

    def filter_min_cost(self, qs, name, value):
        return qs.filter(rate_applied__gte=value)

    def filter_max_cost(self, qs, name, value):
        return qs.filter(rate_applied__lte=value)
