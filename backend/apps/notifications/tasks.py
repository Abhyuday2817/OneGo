from celery import shared_task
from django.utils import timezone
from django.conf import settings
from .models import Notification
from sessions.models import Session

@shared_task
def send_session_reminders():
    """
    Remind both student & mentor 30min before scheduled consultations.
    """
    now = timezone.now()
    window_start = now + timezone.timedelta(minutes=29)
    window_end   = now + timezone.timedelta(minutes=31)
    sessions = Session.objects.filter(
        scheduled_time__gte=window_start,
        scheduled_time__lte=window_end,
        status="scheduled"
    )
    for s in sessions:
        for user in [s.student, s.mentor.user]:
            Notification.objects.create(
                user=user,
                message=f"Your consultation (#{s.pk}) starts at {s.scheduled_time:%H:%M}.",
                link=f"{settings.FRONTEND_URL}/consult/{s.twilio_room_sid}"
            )
