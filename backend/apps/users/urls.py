from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthViewSet, UserViewSet, ChangePasswordView

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")       # 🔐 POST /api/auth/register/ & login/
router.register(r"users", UserViewSet, basename="user")      # 👤 /api/users/... endpoints

urlpatterns = [
    # ViewSets (auth + user)
    path("", include(router.urls)),

    # JWT Token refresh
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Optional: separate password change route (if not using POST /users/me/password/)
    path("auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
]
