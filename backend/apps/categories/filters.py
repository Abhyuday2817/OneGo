import django_filters
from django.db.models import Q
from .models import Category


class CategoryFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(
        choices=Category.TYPE_CHOICES,
        help_text="Filter by category type"
    )
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text="Search by partial name"
    )

    class Meta:
        model = Category
        fields = ['type', 'name']
