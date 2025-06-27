from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category
from .serializers import CategorySerializer
from .filters import CategoryFilter


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Handles full CRUD for course categories.
    Includes top categories, filtering, search, ordering.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CategoryFilter
    search_fields   = ['name', 'description']
    ordering_fields = ['name']
    ordering        = ['name']

    def get_queryset(self):
        """
        Optionally filter by type using ?type=Education etc.
        """
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['get'])
    def top(self, request):
        """
        GET /api/categories/top/
        Returns top 5 categories by number of associated courses.
        """
        top_categories = Category.objects.top_categories(limit=5)
        page = self.paginate_queryset(top_categories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(top_categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def types(self, request):
        """
        GET /api/categories/types/
        Returns the available category types.
        """
        return Response({
            "types": [label for _, label in Category.TYPE_CHOICES]
        })
