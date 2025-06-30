from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MentorReviewViewSet

router = DefaultRouter()
router.register(r'reviews', MentorReviewViewSet, basename='mentor-review')

urlpatterns = [
    path('', include(router.urls)),
]