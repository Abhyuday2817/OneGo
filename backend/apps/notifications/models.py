from django.db import models
from django.utils import timezone
from apps.users.models import User

class Notification(models.Model):
    # Notification Types
    TYPE_INFO = "info"
    TYPE_WARNING = "warning"
    TYPE_ERROR = "error"
    TYPE_CHOICES = [
        (TYPE_INFO, "Info"),
        (TYPE_WARNING, "Warning"),
        (TYPE_ERROR, "Error"),
    ]

    # Priority Levels
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)  # Optional external/internal link
    unread = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_INFO
    )
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        indexes = [
            models.Index(fields=["user", "unread"]),
            models.Index(fields=["type", "priority"]),
        ]

    def __str__(self):
        return f"[{self.type.upper()}] {self.message} → {self.user.username}"

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

    def archive(self):
        if not self.is_archived:
            self.is_archived = True
            self.save()

    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    def save(self, *args, **kwargs):
        # Auto-archive if expired
        if self.is_expired():
            self.is_archived = True
            self.unread = False
        super().save(*args, **kwargs)

    @classmethod
    def mark_all_read(cls, user):
        return cls.objects.filter(user=user, unread=True).update(unread=False)

    @classmethod
    def delete_expired(cls):
        return cls.objects.filter(expires_at__lt=timezone.now()).delete()

    @classmethod
    def unread_for_user(cls, user):
        return cls.objects.filter(user=user, unread=True)

    @classmethod
    def active_for_user(cls, user):
        return cls.objects.filter(user=user, is_archived=False)
