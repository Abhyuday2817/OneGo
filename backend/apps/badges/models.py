from django.db import models
from django.conf import settings
from django.utils import timezone


class Badge(models.Model):
    """
    Represents a badge that can be awarded to users.
    Each badge has a unique slug, name, description, and icon.
    Supports optional level (for gamification) and expiration.
    """
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text="Unique identifier for the badge (used internally)"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_url = models.URLField(
        blank=True,
        help_text="URL or static path to badge image"
    )
    level = models.PositiveIntegerField(
        default=1,
        help_text="Optional badge level for hierarchy (1 = basic, 2 = advanced)"
    )
    expires_in_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Optional: Badge expires after X days from assignment"
    )

    class Meta:
        ordering = ["level", "name"]
        verbose_name = "Badge"
        verbose_name_plural = "Badges"

    def __str__(self):
        return f"{self.name} (Level {self.level})"


class UserBadge(models.Model):
    """
    Tracks which users have earned which badges.
    Supports expiry logic and optional verification.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_badges"
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name="awarded_users"
    )
    awarded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False, help_text="Whether this badge has been verified manually")
    note = models.CharField(max_length=255, blank=True, help_text="Optional note by admin")
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = [["user", "badge"]]
        ordering = ["-awarded_at"]
        verbose_name = "User Badge"
        verbose_name_plural = "User Badges"
        indexes = [
            models.Index(fields=["user", "awarded_at"]),
            models.Index(fields=["badge"]),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.badge.name}"

    def is_active(self):
        """
        Returns True if the badge is currently active (not expired).
        """
        return not self.expires_at or self.expires_at > timezone.now()

    def save(self, *args, **kwargs):
        """
        Auto-calculate `expires_at` based on `badge.expires_in_days`
        """
        if not self.expires_at and self.badge.expires_in_days:
            self.expires_at = self.awarded_at + timezone.timedelta(days=self.badge.expires_in_days)
        super().save(*args, **kwargs)
