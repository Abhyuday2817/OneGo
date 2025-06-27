# mentors/views.py

from django.db import models
from django.db.models import Avg, Count, Q
from rest_framework import viewsets, filters, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as df_filters

from .models import MentorProfile, AvailabilityWindow
from .serializers import MentorProfileSerializer, AvailabilityWindowSerializer


# ──────────────────────────────────────────────────────────────────────────────
# 1) Filtering for Mentor listings
# ──────────────────────────────────────────────────────────────────────────────
class MentorFilter(df_filters.FilterSet):
    rating_min   = df_filters.NumberFilter(field_name="rating", lookup_expr="gte")
    language     = df_filters.CharFilter(field_name="languages", lookup_expr="icontains")
    specialty    = df_filters.NumberFilter(field_name="specialties__id")
    available_at = df_filters.DateTimeFilter(method="filter_availability")

    class Meta:
        model = MentorProfile
        fields = ["rating_min", "language", "specialty"]

    def filter_availability(self, qs, name, value):
        return qs.filter(
            Q(availability_windows__start__lte=value),
            Q(availability_windows__end__gte=value)
        ).distinct()


# ──────────────────────────────────────────────────────────────────────────────
# 2) Mentor List / Detail API
# ──────────────────────────────────────────────────────────────────────────────
class MentorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET  /api/mentors/          → list all mentors (with filters)
    GET  /api/mentors/{pk}/     → retrieve one mentor
    """
    queryset = MentorProfile.objects.prefetch_related("specialties", "user").all()
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_class = MentorFilter
    filter_backends = [df_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields   = ["user__username", "bio"]
    ordering_fields = ["rating", "hourly_rate"]
    ordering        = ["-rating"]

    @action(detail=True, methods=["get"], url_path="availability")
    def availability(self, request, pk=None):
        """
        GET /api/mentors/{pk}/availability/
        Get availability windows of a specific mentor.
        """
        mentor = self.get_object()
        slots = AvailabilityWindow.objects.filter(mentor=mentor).order_by("start")
        serializer = AvailabilityWindowSerializer(slots, many=True)
        return Response(serializer.data)


# ──────────────────────────────────────────────────────────────────────────────
# 3) Mentor Dashboard & Profile Management
# ──────────────────────────────────────────────────────────────────────────────
class MentorDashboardView(APIView):
    """
    GET /api/mentors/dashboard/
    Returns basic analytics for the logged‐in mentor:
      - number of upcoming sessions
      - average student rating
      - total earnings
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = getattr(request.user, "mentor_profile", None)
        if not profile:
            return Response({"detail": "Not a mentor"}, status=status.HTTP_404_NOT_FOUND)

        upcoming = profile.sessions_as_mentor.upcoming().count()
        avg = profile.received_reviews.aggregate(avg=Avg("rating"))["avg"] or 0

        from apps.sessions.models import Session
        earnings = (
            Session.objects.filter(
                mentor=profile,
                status=Session.STATUS_COMPLETED,
                verified=True
            )
            .aggregate(total=models.Sum("rate_applied"))
            .get("total") or 0
        )

        data = {
            "mentor": MentorProfileSerializer(profile, context={"request": request}).data,
            "upcoming_sessions": upcoming,
            "average_rating": round(avg, 2),
            "total_earnings": earnings,
        }
        return Response(data)


class MentorProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/mentors/me/        → retrieve your own profile
    PUT  /api/mentors/me/        → update your own profile
    """
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.mentor_profile


# ──────────────────────────────────────────────────────────────────────────────
# 4) Available Mentors Listing
# ──────────────────────────────────────────────────────────────────────────────
class AvailableMentorsView(generics.ListAPIView):
    """
    GET /api/mentors/available/
    List mentors who currently have at least one open availability window.
    """
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MentorProfile.objects.filter(
            availability_windows__end__gt=models.functions.Now()
        ).distinct()


# ──────────────────────────────────────────────────────────────────────────────
# 5) My Availability Windows (List + Add + Delete)
# ──────────────────────────────────────────────────────────────────────────────
class AvailabilityWindowViewSet(viewsets.ModelViewSet):
    """
    CRUD API for mentor availability slots
    Only available to logged-in mentors
    """
    serializer_class = AvailabilityWindowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AvailabilityWindow.objects.filter(mentor=self.request.user.mentor_profile).order_by("start")

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user.mentor_profile)
