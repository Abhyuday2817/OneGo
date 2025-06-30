from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MentorProfileViewSet,
    MentorProfileDetailView,
    MentorDashboardView,
    AvailableMentorsView,
)

router = DefaultRouter()
router.register(r'', MentorProfileViewSet, basename='mentor')

urlpatterns = [
    path('', include(router.urls)),
    path('me/',          MentorProfileDetailView.as_view(), name='mentor-me'),
    path('dashboard/',   MentorDashboardView.as_view(),     name='mentor-dashboard'),
    path('available/',   AvailableMentorsView.as_view(),    name='mentors-available'),
]
