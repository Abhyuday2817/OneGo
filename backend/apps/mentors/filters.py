from django_filters import rest_framework as filters
from django.db.models import Q
from .models import MentorProfile

class MentorFilter(filters.FilterSet):
    rating_min   = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    language     = filters.CharFilter(field_name='languages', lookup_expr='icontains')
    specialty    = filters.NumberFilter(field_name='specialties__id')
    available_at = filters.DateTimeFilter(method='filter_availability')

    class Meta:
        model = MentorProfile
        fields = ['rating_min', 'language', 'specialty']

    def filter_availability(self, queryset, name, value):
        return queryset.available_at(value)
