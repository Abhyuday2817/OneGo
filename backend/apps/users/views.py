from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsAdmin

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    """
    Handles:
    - POST /api/auth/register/
    - POST /api/auth/login/
    (refresh handled via JWT: /api/auth/token/refresh/)
    """
    permission_classes = [AllowAny]
    serializer_classes = {
        "register": RegisterSerializer,
        "login": LoginSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, RegisterSerializer)

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user, context={"request": request}).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin):
    """
    Admin + user endpoints:
    - GET    /api/users/            (admin only)
    - GET    /api/users/{id}/       (admin only)
    - GET    /api/users/me/         (current user)
    - PATCH  /api/users/me/         (update own info)
    - POST   /api/users/me/password/  (change password)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsAdmin()]
        if self.action in ["me", "password", "partial_update", "update"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "password":
            return ChangePasswordSerializer
        return self.serializer_class

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        GET /api/users/me/
        """
        return Response(
            self.get_serializer(request.user, context={"request": request}).data
        )

    @action(detail=False, methods=["post"], url_path="me/password")
    def password(self, request):
        """
        POST /api/users/me/password/
        {
          "old_password": "current123",
          "new_password": "newpass456"
        }
        """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated."}, status=status.HTTP_200_OK)
