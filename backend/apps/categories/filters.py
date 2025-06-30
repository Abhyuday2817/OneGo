import django_filters
from .models import Category

class CategoryFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(choices=Category.TYPE_CHOICES)
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['type', 'name']
