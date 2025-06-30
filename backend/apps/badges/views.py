from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoint to view all badge definitions.
    GET /api/badges/ — list all badges
    GET /api/badges/{id}/ — retrieve badge by ID
    """
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Authenticated users can view their own earned badges.
    GET /api/user-badges/ — badges for current user
    """
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """
        GET /api/user-badges/recent/ — recently earned badges (last 5)
        """
        recent_badges = UserBadge.objects.filter(user=request.user).order_by('-awarded_at')[:5]
        serializer = self.get_serializer(recent_badges, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ViewSet):
    """
    Leaderboard API showing top users by number of badges earned.
    GET /api/badges/leaderboard/
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        top_users = (
            UserBadge.objects
            .values("user__username")
            .annotate(badge_count=Count("badge"))
            .order_by("-badge_count")[:10]
        )
        return Response(top_users)

    @action(detail=False, methods=["get"])
    def full(self, request):
        """
        GET /api/badges/leaderboard/full/ — full leaderboard
        """
        all_users = (
            UserBadge.objects
            .values("user__username")
            .annotate(badge_count=Count("badge"))
            .order_by("-badge_count")
        )
        return Response(all_users)
