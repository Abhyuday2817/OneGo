from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

# DRF Router setup
router = DefaultRouter()
router.register(r"", NotificationViewSet, basename="notification")

urlpatterns = [
    # All notification endpoints like:
    # /api/notifications/
    # /api/notifications/{id}/
    # /api/notifications/{id}/mark-read/
    # /api/notifications/mark-all-read/
    # /api/notifications/unread-count/
    path("", include(router.urls)),
]
