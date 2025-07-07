# apps/enrollments/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment
from apps.notifications.models import Notification
from django.utils import timezone

@receiver(post_save, sender=Enrollment)
def handle_enrollment_created(sender, instance, created, **kwargs):
    if created:
        # Optional: Send notification to mentor when a student enrolls
        mentor_user = instance.course.mentor.user
        Notification.objects.create(
            user=mentor_user,
            message=f"{instance.student.username} enrolled in your course: {instance.course.title}",
            link=f"/courses/{instance.course.slug}/",
            type="enrollment",
            expires_at=timezone.now() + timezone.timedelta(days=7)
        )

        # Optional: Print to console for debug
        print(f"📚 New enrollment: {instance.student.username} → {instance.course.title}")
