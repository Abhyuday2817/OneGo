# apps/courses/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet  # ✅ Removed CourseQuizViewSet

router = DefaultRouter()
router.register(r"", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
