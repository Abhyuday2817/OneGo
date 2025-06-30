# backend/services/notifications.py

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from apps.notifications.models import Notification

# Optional: Twilio / Push / Logging
import logging

logger = logging.getLogger(__name__)

# ----- BASIC IN-APP NOTIFICATION -----
def notify_user(user, message: str, link: str = ""):
    try:
        Notification.objects.create(user=user, message=message, link=link)
        logger.info(f"Notification sent to {user.username}")
    except Exception as e:
        logger.error(f"Failed to notify user {user.username}: {e}")


# ----- EMAIL NOTIFICATION -----
def send_email_notification(user, subject: str, message: str):
    try:
        if not user.email:
            raise ValueError("User has no email address")
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        logger.info(f"Email sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send email to {user.username}: {e}")


# ----- SMS NOTIFICATION (STUB / Twilio-ready) -----
def send_sms_notification(phone_number: str, body: str):
    try:
        # Integrate with Twilio or any other SMS provider here
        logger.info(f"SMS sent to {phone_number}: {body}")
    except Exception as e:
        logger.error(f"Failed to send SMS to {phone_number}: {e}")


# ----- PUSH NOTIFICATION (STUB / FCM-Ready) -----
def send_push_notification(user, title: str, body: str, data: dict = None):
    try:
        # Implement Firebase Cloud Messaging or APNs logic here
        logger.info(f"Push sent to {user.username}: {title} - {body}")
    except Exception as e:
        logger.error(f"Failed to send push to {user.username}: {e}")


# ----- BULK NOTIFICATION -----
def bulk_notify(users, message: str, link: str = ""):
    for user in users:
        notify_user(user, message, link)


# ----- OPTIONAL LOGGING FOR AUDIT -----
def log_notification(user, method: str, message: str, extra: dict = None):
    log = {
        "user": user.username,
        "method": method,
        "message": message,
        "timestamp": timezone.now().isoformat(),
        "extra": extra or {},
    }
    logger.info(f"[AUDIT][{method}] {log}")
