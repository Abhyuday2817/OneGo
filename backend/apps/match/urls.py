from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet

router = DefaultRouter()
# register under “match”, so:
#   /api/match/mentors/
#   /api/match/courses/
router.register(r'', MatchViewSet, basename='match')

urlpatterns = [
    path('', include(router.urls)),
]
