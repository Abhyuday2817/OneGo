from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, UserBadgeViewSet, LeaderboardView

router = DefaultRouter()
router.register("badges", BadgeViewSet, basename="badge")
router.register("my-badges", UserBadgeViewSet, basename="user-badge")
router.register("leaderboard", LeaderboardView, basename="leaderboard")

urlpatterns = [
    path("", include(router.urls)),
]
