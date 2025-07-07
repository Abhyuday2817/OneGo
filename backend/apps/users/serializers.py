from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import StudentProfile

User = get_user_model()

# ──────────────────────────────────────────────────────────────────────────────
# 🔹 Minimal user serializer for nested use
# ──────────────────────────────────────────────────────────────────────────────
class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


# ──────────────────────────────────────────────────────────────────────────────
# 🔹 Main user profile serializer
# ──────────────────────────────────────────────────────────────────────────────
class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "role", "bio", "avatar_url", "languages", "location",
            "hourly_rate", "per_minute_rate",
        ]
        read_only_fields = ["id", "role", "avatar_url"]

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None


# ──────────────────────────────────────────────────────────────────────────────
# 🔹 User registration serializer
# ──────────────────────────────────────────────────────────────────────────────
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    role = serializers.ChoiceField(choices=User.Role.choices)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username", "email",
            "password1", "password2",
            "first_name", "last_name",
            "role"
        ]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        password_validation.validate_password(attrs["password1"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password1")
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        # Auto-create student profile if role is student
        if user.role == User.Role.STUDENT:
            StudentProfile.objects.get_or_create(user=user)
        return user


# ──────────────────────────────────────────────────────────────────────────────
# 🔹 Login serializer
# ──────────────────────────────────────────────────────────────────────────────
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


# ──────────────────────────────────────────────────────────────────────────────
# 🔹 Change password serializer
# ──────────────────────────────────────────────────────────────────────────────
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={"input_type": "password"})
    new_password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_new_password(self, pw):
        password_validation.validate_password(pw, self.context["request"].user)
        return pw

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": "Wrong password."})
        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


# ──────────────────────────────────────────────────────────────────────────────
# 🔹 Student profile serializer
# ──────────────────────────────────────────────────────────────────────────────
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "photo", "education", "interests", "learning_goals",
            "language_preference", "budget_range"
        ]
