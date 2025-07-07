from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    StudentProfileSerializer
)
from .models import StudentProfile
from .permissions import IsAdmin

User = get_user_model()

# 🔹 1. AuthViewSet (Register + Login)
class AuthViewSet(viewsets.GenericViewSet):
    """
    🔐 Handles:
    - POST /api/auth/register/
    - POST /api/auth/login/
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


# 🔹 2. UserViewSet (Admin & User Profile)
class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin):
    """
    🙋‍♂️ Admin + User endpoints:
    - GET    /api/users/                      (admin only)
    - GET    /api/users/{id}/                 (admin only)
    - GET    /api/users/me/                   (current user info)
    - PATCH  /api/users/me/                   (update own info)
    - POST   /api/users/me/password/          (change password)
    - GET/PUT /api/users/me/student-profile/  (student profile CRUD)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # default global permission

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsAdmin()]
        if self.action in ["me", "password", "student_profile"]:
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
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="me/password")
    def password(self, request):
        """
        POST /api/users/me/password/
        Payload: {"old_password": "...", "new_password": "..."}
        """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get", "put"], url_path="me/student-profile")
    def student_profile(self, request):
        """
        - GET /api/users/me/student-profile/
        - PUT /api/users/me/student-profile/
        """
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)

        if request.method == "GET":
            return Response(StudentProfileSerializer(profile).data)

        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# 🔹 3. ChangePasswordView (if separate endpoint)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
