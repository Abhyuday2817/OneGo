from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    # JWT refresh
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
