# courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register(r"", CourseViewSet, basename="course")

urlpatterns = [
    # /api/courses/ → list, create ; /api/courses/{pk}/ → retrieve, update, delete
    path("", include(router.urls)),
]
