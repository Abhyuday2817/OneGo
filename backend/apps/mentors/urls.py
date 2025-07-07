from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MentorProfileViewSet,
    MentorDashboardView,
    MentorProfileDetailView,
    AvailableMentorsView,
    AvailabilityWindowViewSet,
    MentorAvailabilityViewSet,
    MentorStatsView,
)

router = DefaultRouter()
router.register(r'mentors', MentorProfileViewSet, basename='mentor')
router.register(r'availability-windows', AvailabilityWindowViewSet, basename='availability-window')
router.register(r'weekly-availability', MentorAvailabilityViewSet, basename='weekly-availability')

urlpatterns = [
    path('', include(router.urls)),
    path('me/', MentorProfileDetailView.as_view(), name='mentor-me'),
    path('available/', AvailableMentorsView.as_view(), name='mentor-available'),
    path('dashboard/', MentorDashboardView.as_view(), name='mentor-dashboard'),
    path('stats/', MentorStatsView.as_view(), name='mentor-stats'),
    path('mentors/<int:pk>/availability/', MentorProfileViewSet.as_view({'get': 'availability'}), name='mentor-availability'),
    path('mentors/<int:pk>/book-slot/', MentorProfileViewSet.as_view({'post': 'book_slot'}), name='mentor-book-slot'),
]