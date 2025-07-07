from django.db import models
from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte", label="Min Price")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte", label="Max Price")
    delivery_type = filters.ChoiceFilter(field_name="delivery_type", choices=Course.DELIVERY_CHOICES)
    category = filters.NumberFilter(field_name="category_id")
    mentor = filters.NumberFilter(field_name="mentor_id")
    search = filters.CharFilter(method="filter_search", label="Keyword")

    class Meta:
        model = Course
        fields = ["category", "delivery_type", "price_min", "price_max", "mentor"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(mentor__user__username__icontains=value)
        )
