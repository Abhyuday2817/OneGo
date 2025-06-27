from django.db import models
from django.conf import settings


class Badge(models.Model):
    """
    Represents a badge definition that can be awarded to users.
    Includes a unique slug, name, description, and optional icon URL.
    """
    slug        = models.SlugField(max_length=50, unique=True, help_text="Unique code for badge programmatic access")
    name        = models.CharField(max_length=100)
    description = models.TextField()
    icon_url    = models.URLField(blank=True, help_text="Optional: URL or static path to the badge icon")

    class Meta:
        ordering = ["name"]
        verbose_name = "Badge"
        verbose_name_plural = "Badges"

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """
    Tracks when a user has been awarded a badge.
    """
    user       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_badges"
    )
    badge      = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name="awarded_to"
    )
    awarded_at = models.DateTimeField(auto_now_add=True)

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
        return f"{self.user.username} → {self.badge.slug}"
