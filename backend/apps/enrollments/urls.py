from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet

# Register EnrollmentViewSet with router
router = DefaultRouter()
router.register(r"", EnrollmentViewSet, basename="enrollment")

urlpatterns = [
    path("", include(router.urls)),
]
