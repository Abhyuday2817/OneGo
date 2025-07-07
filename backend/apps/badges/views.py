from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Badge, UserBadge
from .serializers import (
    BadgeSerializer,
    UserBadgeSerializer,
    AssignUserBadgeSerializer,
    VerifyBadgeSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoint to view all badge definitions.
    GET /api/badges/ — list all badges
    GET /api/badges/{id}/ — retrieve badge by ID
    """
    queryset = Badge.objects.all().order_by('level', 'name')
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def levels(self, request):
        """
        GET /api/badges/levels/ — badge levels with counts
        """
        level_counts = (
            Badge.objects.values("level")
            .annotate(total=Count("id"))
            .order_by("level")
        )
        return Response(level_counts)


class UserBadgeViewSet(viewsets.ModelViewSet):
    """
    Authenticated users can:
    - View their badges (GET)
    - Admins can assign or verify (POST/PUT)
    """
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and self.action in ["list", "retrieve"]:
            return UserBadge.objects.select_related("user", "badge").all()
        return UserBadge.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def my(self, request):
        """
        GET /api/user-badges/my/ — current user’s earned badges
        """
        qs = UserBadge.objects.filter(user=request.user).select_related("badge")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """
        GET /api/user-badges/recent/ — last 5 earned badges
        """
        qs = UserBadge.objects.filter(user=request.user).order_by("-awarded_at")[:5]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def assign(self, request):
        """
        POST /api/user-badges/assign/
        Admin: Assign badge to user
        Payload: { "user": user_id, "badge": badge_id, "note": "" }
        """
        serializer = AssignUserBadgeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_badge = serializer.save()
        return Response(UserBadgeSerializer(user_badge).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], permission_classes=[permissions.IsAdminUser])
    def verify(self, request, pk=None):
        """
        PATCH /api/user-badges/{id}/verify/
        Admin: mark badge as verified
        Payload: { "verified": true }
        """
        badge_instance = self.get_object()
        serializer = VerifyBadgeSerializer(badge_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserBadgeSerializer(badge_instance).data)


class LeaderboardViewSet(viewsets.ViewSet):
    """
    Leaderboard API: show users with most badges
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        """
        GET /api/badges/leaderboard/
        Top 10 users by badge count
        """
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
        GET /api/badges/leaderboard/full/
        All users sorted by badge count
        """
        all_users = (
            UserBadge.objects
            .values("user__username")
            .annotate(badge_count=Count("badge"))
            .order_by("-badge_count")
        )
        return Response(all_users)
