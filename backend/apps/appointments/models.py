# apps/appointments/models.py

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

from apps.mentors.models import MentorProfile

# ---------- Appointment Status Choices ----------
STATUS_PENDING = "pending"
STATUS_CONFIRMED = "confirmed"
STATUS_COMPLETED = "completed"
STATUS_CANCELED = "canceled"
STATUS_NO_SHOW = "no_show"
STATUS_RESCHEDULED = "rescheduled"

STATUS_CHOICES = [
    (STATUS_PENDING, "Pending"),
    (STATUS_CONFIRMED, "Confirmed"),
    (STATUS_COMPLETED, "Completed"),
    (STATUS_CANCELED, "Canceled"),
    (STATUS_NO_SHOW, "No Show"),
    (STATUS_RESCHEDULED, "Rescheduled"),
]


# ---------- Custom Manager ----------
class AppointmentManager(models.Manager):
    def upcoming(self):
        return self.filter(start_time__gte=timezone.now(), status__in=[STATUS_PENDING, STATUS_CONFIRMED]).order_by("start_time")

    def past(self):
        return self.filter(end_time__lt=timezone.now()).exclude(status__in=[STATUS_CANCELED, STATUS_NO_SHOW]).order_by("-start_time")

    def today(self):
        now = timezone.now()
        return self.filter(start_time__date=now.date())

    def for_mentor(self, mentor):
        return self.filter(mentor=mentor)

    def for_student(self, student):
        return self.filter(student=student)


# ---------- Main Appointment Model ----------
class Appointment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AppointmentManager()

    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['mentor', 'start_time']),
            models.Index(fields=['student', 'start_time']),
        ]
        unique_together = ("mentor", "start_time", "end_time")

    def __str__(self):
        return f"{self.student.username} ↔ {self.mentor.user.username} @ {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def duration(self):
        return self.end_time - self.start_time

    def get_status_display(self):
        return dict(STATUS_CHOICES).get(self.status, self.status)

    def is_conflict(self):
        return Appointment.objects.filter(
            mentor=self.mentor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk).exists()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        if not (9 <= self.start_time.hour < 18 and 9 <= self.end_time.hour <= 18):
            raise ValidationError("Appointment must be within working hours (9am–6pm).")

        if self.is_conflict():
            raise ValidationError("Mentor already has an appointment in this time slot.")

    def cancel(self):
        self.status = STATUS_CANCELED
        self.save()

    def reschedule(self, new_start, new_end):
        self.start_time = new_start
        self.end_time = new_end
        self.status = STATUS_RESCHEDULED
        self.full_clean()
        self.save()

    def save(self, *args, **kwargs):
        #self.full_clean()
        super().save(*args, **kwargs)
