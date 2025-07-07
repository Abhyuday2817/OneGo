# apps/consultations/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet

router = DefaultRouter()
router.register(r"", ConsultationViewSet, basename="consultation")

urlpatterns = [
    # Base routes: /api/consultations/
    path("", include(router.urls)),
]
