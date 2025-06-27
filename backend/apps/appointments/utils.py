# apps/appointments/utils.py

from django.core.mail import send_mail
from django.http import HttpResponse
import csv
from django.db.models import Count
from apps.mentors.models import MentorProfile
from .models import Appointment

# ---- Reminders ----
def send_appointment_reminder(appointment):
    """Send an email reminder for the appointment."""
    send_mail(
        subject="Upcoming Appointment Reminder",
        message=(
            f"Dear {appointment.student.get_full_name()},\n\n"
            f"This is a reminder for your upcoming appointment with mentor"
            f" {appointment.mentor.user.get_full_name()} on {appointment.start_time}.\n\n"
            "Best regards,\nOneGo Team"
        ),
        from_email="noreply@onego.app",
        recipient_list=[appointment.student.email],
        fail_silently=False,
    )


# ---- CSV Export ----
def export_appointments_csv(queryset):
    """Export a queryset of appointments to CSV."""
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


# ---- Analytics ----
def get_mentor_appointment_count(mentor, start=None, end=None):
    """Return the number of appointments for a given mentor, optionally within a time range."""
    qs = mentor.appointments.all()
    if start:
        qs = qs.filter(start_time__gte=start)
    if end:
        qs = qs.filter(start_time__lte=end)
    return qs.count()


def get_most_booked_mentors(top_n=5):
    """Return top mentors by number of appointments."""
    return (
        MentorProfile.objects
        .annotate(num_appointments=Count('appointments'))
        .order_by('-num_appointments')[:top_n]
    )


def get_busiest_days(days=7):
    """Return busiest days based on number of appointments."""
    return (
        Appointment.objects
        .values('start_time__date')
        .annotate(num_appointments=Count('id'))
        .order_by('-num_appointments')[:days]
    )


# ---- Google Calendar Sync (stub) ----
def add_to_google_calendar(appointment, credentials_data):
    """Stub for Google Calendar sync - not implemented yet."""
    # Integrate with Google Calendar API here
    pass


# ---- SMS Reminder (stub) ----
def send_sms_reminder(to_number, body):
    """Stub for SMS reminder - not implemented yet."""
    # Integrate with SMS provider (e.g., Twilio)
    pass
