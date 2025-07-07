from django.db.models import Avg, Q, Sum
from django.utils import timezone
from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework import viewsets, filters, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as df_filters

from .models import MentorProfile, AvailabilityWindow, MentorAvailability
from .serializers import (
    MentorProfileSerializer,
    MentorProfileListSerializer,
    AvailabilityWindowSerializer,
    MentorAvailabilitySerializer,
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MentorFilter(df_filters.FilterSet):
    rating_min = df_filters.NumberFilter(field_name="rating", lookup_expr="gte")
    rating_max = df_filters.NumberFilter(field_name="rating", lookup_expr="lte")
    language = df_filters.CharFilter(field_name="languages", lookup_expr="icontains")
    specialty = df_filters.NumberFilter(field_name="specialties__id")
    country = df_filters.CharFilter(field_name="country", lookup_expr="iexact")
    hourly_rate_min = df_filters.NumberFilter(field_name="hourly_rate", lookup_expr="gte")
    hourly_rate_max = df_filters.NumberFilter(field_name="hourly_rate", lookup_expr="lte")
    is_verified = df_filters.BooleanFilter(field_name="is_verified")
    available_at = df_filters.DateTimeFilter(method="filter_availability")

    class Meta:
        model = MentorProfile
        fields = ["rating_min", "rating_max", "language", "specialty", "country", 
                 "hourly_rate_min", "hourly_rate_max", "is_verified"]

    def filter_availability(self, qs, name, value):
        return qs.filter(
            Q(availability_windows__start__lte=value),
            Q(availability_windows__end__gte=value),
            Q(availability_windows__is_booked=False)
        ).distinct()

class MentorProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = MentorFilter
    filter_backends = [df_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["user__username", "user__first_name", "user__last_name", "bio", "expertise"]
    ordering_fields = ["rating", "hourly_rate", "per_minute_rate", "created_at"]
    ordering = ["-rating", "-is_verified"]
    pagination_class = StandardResultsSetPagination
    queryset = MentorProfile.objects.none()  # Required for ModelViewSet, overridden in get_queryset

    def get_queryset(self):
        return MentorProfile.objects.filter(
            is_active=True
        ).with_stats()

    def get_serializer_class(self):
        if self.action == 'list':
            return MentorProfileListSerializer
        return MentorProfileSerializer

    @action(detail=True, methods=["get"], url_path="availability")
    def availability(self, request, pk=None):
        mentor = self.get_object()
        cache_key = f"mentor_availability_{pk}"
        cached_data = cache.get(cache_key)
        if cached_data is None:
            slots = AvailabilityWindow.objects.filter(
                mentor=mentor,
                start__gt=timezone.now(),
                is_booked=False
            ).order_by("start")
            serializer = AvailabilityWindowSerializer(slots, many=True)
            cached_data = serializer.data
            cache.set(cache_key, cached_data, 300)
        return Response(cached_data)

    @action(detail=True, methods=["post"], url_path="book-slot")
    def book_slot(self, request, pk=None):
        mentor = self.get_object()
        slot_id = request.data.get('slot_id')
        try:
            slot = AvailabilityWindow.objects.get(
                id=slot_id, 
                mentor=mentor, 
                is_booked=False,
                start__gt=timezone.now()
            )
            slot.is_booked = True
            slot.save()
            cache.delete(f"mentor_availability_{pk}")
            return Response({"message": "Slot booked successfully"})
        except AvailabilityWindow.DoesNotExist:
            return Response(
                {"error": "Slot not available"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class MentorDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.mentor_profile
        except MentorProfile.DoesNotExist:
            return Response(
                {"detail": "User is not a mentor"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        # Calculate stats
        try:
            from apps.sessions.models import Session
            upcoming = Session.objects.filter(
                mentor=profile,
                start_time__gte=timezone.now(),
                status='scheduled'
            ).count()
            earnings = Session.objects.filter(
                mentor=profile,
                status='completed',
                verified=True
            ).aggregate(total=Sum("rate_applied"))['total'] or 0
        except ImportError:
            upcoming = 0
            earnings = 0
        # Get reviews if available
        try:
            from apps.reviews.models import Review
            avg_rating = Review.objects.filter(
                mentor=profile
            ).aggregate(avg=Avg("rating"))['avg'] or 0
        except ImportError:
            avg_rating = profile.rating
        data = {
            "mentor": MentorProfileSerializer(profile, context={"request": request}).data,
            "upcoming_sessions": upcoming,
            "average_rating": round(avg_rating, 2),
            "total_earnings": round(float(earnings), 2),
            "this_month_earnings": 0,
            "total_sessions": 0,
        }
        return Response(data)

class MentorProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MentorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']
    def get_object(self):
        try:
            return self.request.user.mentor_profile
        except MentorProfile.DoesNotExist:
            raise ValidationError("User does not have a mentor profile")
    def perform_update(self, serializer):
        serializer.save()
        cache.delete(f"mentor_availability_{serializer.instance.id}")

class AvailableMentorsView(generics.ListAPIView):
    serializer_class = MentorProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):
        return MentorProfile.objects.filter(
            is_active=True,
            availability_windows__end__gt=timezone.now(),
            availability_windows__is_booked=False
        ).distinct().with_stats()

class AvailabilityWindowViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilityWindowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'mentor_profile'):
            return AvailabilityWindow.objects.none()
        return AvailabilityWindow.objects.filter(
            mentor=user.mentor_profile
        ).order_by("start")

    def perform_create(self, serializer):
        mentor = self.request.user.mentor_profile
        serializer.save(mentor=mentor)
        cache.delete(f"mentor_availability_{mentor.id}")

    def perform_update(self, serializer):
        mentor = self.request.user.mentor_profile
        serializer.save()
        cache.delete(f"mentor_availability_{mentor.id}")

    def perform_destroy(self, instance):
        mentor_id = instance.mentor.id
        instance.delete()
        cache.delete(f"mentor_availability_{mentor_id}")

class MentorAvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = MentorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'mentor_profile'):
            return MentorAvailability.objects.none()
        return MentorAvailability.objects.filter(
            mentor=user.mentor_profile
        ).order_by("day", "start_time")

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user.mentor_profile)

class MentorStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            profile = request.user.mentor_profile
        except MentorProfile.DoesNotExist:
            return Response(
                {"detail": "User is not a mentor"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        stats = {
            "total_students": profile.total_students_taught(),
            "total_earnings": float(profile.total_earnings()),
            "average_session_duration": profile.average_session_duration(),
            "upcoming_sessions": profile.get_upcoming_sessions().count(),
            "available_slots": profile.availability_windows.filter(
                start__gt=timezone.now(),
                is_booked=False
            ).count(),
            "rating": profile.rating,
            "num_reviews": profile.num_reviews,
        }
        return Response(stats)