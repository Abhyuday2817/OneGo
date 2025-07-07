# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# ──────────────────────────────────────────────────────────────────────────────
# User Model
# ──────────────────────────────────────────────────────────────────────────────

class User(AbstractUser):
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

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    languages = models.JSONField(default=list, blank=True, help_text=_("List of ISO language codes."))
    location = models.CharField(max_length=255, blank=True)

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
        return self.role == self.Role.ADMIN or self.is_staff

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "User"
        verbose_name_plural = "Users"


# ──────────────────────────────────────────────────────────────────────────────
# Student Profile
# ──────────────────────────────────────────────────────────────────────────────

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    learning_goals = models.TextField(null=True, blank=True)
    language_preference = models.CharField(max_length=100, null=True, blank=True)
    budget_range = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"StudentProfile: {self.user.username}"

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"


# ──────────────────────────────────────────────────────────────────────────────
# Auto-create StudentProfile if user is student
# ──────────────────────────────────────────────────────────────────────────────

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.STUDENT:
        StudentProfile.objects.get_or_create(user=instance)
