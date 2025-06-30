from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    list/retrieve/create/update/delete reviews.
    - Only authenticated users can create
    - Reviewers can only update/delete their own reviews
    """
    queryset = Review.objects.select_related('reviewer', 'reviewee__user').all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    search_fields = ['reviewee__user__username', 'reviewer__username']

    def get_queryset(self):
        # Users can see reviews they've written or received
        user = self.request.user
        return self.queryset.filter(
            reviewer=user
        ) | self.queryset.filter(
            reviewee__user=user
        )

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.reviewer != request.user:
            raise PermissionDenied("You can only update your own reviews.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if review.reviewer != request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        return super().destroy(request, *args, **kwargs)
