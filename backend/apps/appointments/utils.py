# apps/appointments/utils.py

import csv
from django.core.mail import send_mail
from django.http import HttpResponse
from django.db.models import Count
from django.utils import timezone

from .models import Appointment
from apps.mentors.models import MentorProfile

# ─────────────────────────────────────────────────────
# 📧 Email Reminder
# ─────────────────────────────────────────────────────

def send_appointment_reminder(appointment):
    """
    Sends an email reminder to the student about an upcoming appointment.
    """
    send_mail(
        subject="⏰ Appointment Reminder - OneGo",
        message=(
            f"Hi {appointment.student.get_full_name()},\n\n"
            f"This is a reminder for your appointment with mentor "
            f"{appointment.mentor.user.get_full_name()} scheduled on "
            f"{appointment.start_time.strftime('%A, %d %B %Y at %I:%M %p')}.\n\n"
            "Prepare your questions and join on time!\n\n"
            "— Team OneGo"
        ),
        from_email="noreply@onego.app",
        recipient_list=[appointment.student.email],
        fail_silently=False,
    )

# ─────────────────────────────────────────────────────
# 📁 CSV Export
# ─────────────────────────────────────────────────────

def export_appointments_csv(queryset):
    """
    Exports a queryset of appointments into a downloadable CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student', 'Mentor', 'Start Time', 'End Time', 'Status'])

    for appt in queryset:
        writer.writerow([
            appt.student.get_full_name(),
            appt.mentor.user.get_full_name(),
            appt.start_time.strftime('%Y-%m-%d %H:%M'),
            appt.end_time.strftime('%Y-%m-%d %H:%M'),
            appt.get_status_display(),
        ])

    return response

# ─────────────────────────────────────────────────────
# 📊 Analytics
# ─────────────────────────────────────────────────────

def get_mentor_appointment_count(mentor, start=None, end=None):
    """
    Returns appointment count for a given mentor within an optional date range.
    """
    qs = mentor.appointments.all()
    if start:
        qs = qs.filter(start_time__gte=start)
    if end:
        qs = qs.filter(start_time__lte=end)
    return qs.count()


def get_most_booked_mentors(top_n=5):
    """
    Returns the top N mentors ordered by number of appointments.
    """
    return (
        MentorProfile.objects
        .annotate(num_appointments=Count('appointments'))
        .order_by('-num_appointments')[:top_n]
    )


def get_busiest_days(days=7):
    """
    Returns the busiest days (in last N days) by total appointments scheduled.
    """
    return (
        Appointment.objects
        .values('start_time__date')
        .annotate(num_appointments=Count('id'))
        .order_by('-num_appointments')[:days]
    )

# ─────────────────────────────────────────────────────
# 🔁 Auto Status Update
# ─────────────────────────────────────────────────────

def auto_mark_past_appointments_completed():
    """
    Mark confirmed appointments in the past as 'completed'.
    Useful for scheduled jobs or CRON tasks.
    """
    past_qs = Appointment.objects.filter(
        end_time__lt=timezone.now(),
        status="confirmed"
    )
    updated_count = past_qs.update(status="completed")
    return updated_count

# ─────────────────────────────────────────────────────
# 📆 Google Calendar Integration (Stub)
# ─────────────────────────────────────────────────────

def add_to_google_calendar(appointment, credentials_data=None):
    """
    Stub: Add appointment to Google Calendar via API.
    Accepts appointment instance and OAuth credentials data.
    """
    # Integration example:
    # from googleapiclient.discovery import build
    # service = build('calendar', 'v3', credentials=credentials)
    # service.events().insert(calendarId='primary', body=event).execute()
    print(f"[Stub] Add to Google Calendar: {appointment}")
    return None

# ─────────────────────────────────────────────────────
# 📱 SMS Reminder (Stub)
# ─────────────────────────────────────────────────────

def send_sms_reminder(to_number, message):
    """
    Stub: Send SMS reminder using a provider like Twilio or Fast2SMS.
    """
    # Example placeholder:
    # client.messages.create(to=to_number, body=message, from_="OneGo")
    print(f"[Stub] SMS to {to_number}: {message}")
    return None
