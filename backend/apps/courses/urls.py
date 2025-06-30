from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CourseQuizViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"quizzes", CourseQuizViewSet, basename="quiz")

urlpatterns = [
    # List/create courses:      /api/courses/courses/
    # Retrieve/update course:   /api/courses/courses/{id}/
    # List quizzes:             /api/courses/quizzes/
    # Retrieve quiz:            /api/courses/quizzes/{id}/
    path("", include(router.urls)),
]
