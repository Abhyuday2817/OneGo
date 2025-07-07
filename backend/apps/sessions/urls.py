from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet

# Register SessionViewSet with DRF router
router = DefaultRouter()
router.register(r"sessions", SessionViewSet, basename="session")

urlpatterns = [
    path("", include(router.urls)),
]
