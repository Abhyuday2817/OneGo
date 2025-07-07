from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategorySerializer
from .filters import CategoryFilter


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for course categories.
    Provides filtering, searching, ordering, and special endpoints.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CategoryFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'type']
    ordering = ['name']

    def get_queryset(self):
        """
        Optional filtering:
        - /api/categories/?type=Education
        - /api/categories/?has_free=true
        """
        qs = super().get_queryset()
        has_free = self.request.query_params.get("has_free")
        if has_free is not None:
            if has_free.lower() == "true":
                qs = [c for c in qs if c.has_free_courses()]
            elif has_free.lower() == "false":
                qs = [c for c in qs if not c.has_free_courses()]
        return qs

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
        Returns top 5 categories by number of courses.
        """
        try:
            top_categories = Category.objects.top_categories(limit=5)
            page = self.paginate_queryset(top_categories)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(top_categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def types(self, request):
        """
        GET /api/categories/types/
        Returns available category types for dropdowns.
        """
        return Response({
            "types": [{"value": val, "label": label} for val, label in Category.TYPE_CHOICES]
        })
