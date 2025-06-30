from django.utils.timezone import now
from notifications.models import Notification
from users.models import User


def send_notification(user: User, title: str, message: str, related_object=None):
    """
    Create and send a notification to a user.
    Optionally attach a related object (like a session or booking).
    """
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        timestamp=now(),
        related_object=related_object
    )


def notify_session_booking(student: User, mentor: User, session):
    """
    Notify both student and mentor when a session is booked.
    """
    send_notification(
        user=student,
        title="Session Booked",
        message=f"Your session with {mentor.get_full_name()} has been booked.",
        related_object=session
    )
    send_notification(
        user=mentor,
        title="New Booking",
        message=f"You have a new session booked with {student.get_full_name()}.",
        related_object=session
    )


def notify_session_reminder(user: User, session):
    """
    Notify user about upcoming session reminder.
    """
    send_notification(
        user=user,
        title="Session Reminder",
        message=f"Reminder: Your session '{session.title}' is starting soon.",
        related_object=session
    )
