from django.db import models
from django.utils import timezone
from apps.users.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)  # Optional link for the notification
    unread = models.BooleanField(default=True)  # Field indicating if the notification is unread
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium"
    )
    expires_at = models.DateTimeField(blank=True, null=True)
    type = models.CharField(
        max_length=20,
        choices=[("info", "Info"), ("warning", "Warning"), ("error", "Error")],
        default="info"
    )
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    def mark_as_read(self):
        self.unread = False
        self.save()

    def archive(self):
        self.is_archived = True
        self.save()

    @classmethod
    def get_expired(cls):
        return cls.objects.filter(expires_at__lt=timezone.now())