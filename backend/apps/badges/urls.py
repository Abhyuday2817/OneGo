from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, UserBadgeViewSet, LeaderboardViewSet

router = DefaultRouter()
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'user-badges', UserBadgeViewSet, basename='user-badge')
router.register(r'badges/leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path("", include(router.urls)),
]
