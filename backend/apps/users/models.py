# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser,
    with support for role-based access and additional profile fields.
    """

    class Role(models.TextChoices):
        STUDENT = "student", _("Student")
        MENTOR  = "mentor",  _("Mentor")
        ADMIN   = "admin",   _("Admin")

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text=_("Designates whether the user is a student, mentor, or admin.")
    )

    # Common profile fields
    bio       = models.TextField(blank=True)
    avatar    = models.ImageField(upload_to="avatars/", blank=True, null=True)
    languages = models.JSONField(default=list, blank=True, help_text=_("List of ISO language codes."))
    location  = models.CharField(max_length=255, blank=True)

    # Mentor-specific fields (optional)
    hourly_rate = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=_("Optional hourly rate if user is a mentor.")
    )
    per_minute_rate = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=_("Optional per-minute rate if user is a mentor.")
    )

    def is_student(self) -> bool:
        return self.role == self.Role.STUDENT

    def is_mentor(self) -> bool:
        return self.role == self.Role.MENTOR

    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
