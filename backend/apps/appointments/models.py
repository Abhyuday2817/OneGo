# apps/appointments/models.py

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.users.models import User
from apps.mentors.models import MentorProfile

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("canceled", "Canceled"),
    ("completed", "Completed"),
    ("no_show", "No Show"),
    ("rescheduled", "Rescheduled"),
]


class AppointmentManager(models.Manager):
    def upcoming(self):
        return self.filter(start_time__gte=timezone.now()).order_by("start_time")

    def past(self):
        return self.filter(end_time__lt=timezone.now()).order_by("-start_time")

    def today(self):
        now = timezone.now()
        return self.filter(start_time__date=now.date())

    def for_mentor(self, mentor):
        return self.filter(mentor=mentor)

    def for_student(self, student):
        return self.filter(student=student)


class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AppointmentManager()

    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['mentor', 'start_time']),
            models.Index(fields=['student', 'start_time']),
        ]

    def __str__(self):
        return f"{self.student} with {self.mentor} @ {self.start_time:%Y-%m-%d %H:%M}"

    def is_conflict(self):
        overlapping = Appointment.objects.filter(
            mentor=self.mentor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)
        return overlapping.exists()

    def duration(self):
        return self.end_time - self.start_time

    def cancel(self):
        self.status = 'canceled'
        self.save()

    def reschedule(self, new_start, new_end):
        self.start_time = new_start
        self.end_time = new_end
        self.status = 'rescheduled'
        self.save()

    def get_status_display(self):
        return dict(STATUS_CHOICES).get(self.status, self.status)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        # Prevent double-booking
        if Appointment.objects.filter(
            mentor=self.mentor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk).exists():
            raise ValidationError("This slot is already booked for the mentor.")

        # Working hours check: 9 AM to 6 PM
        if not (9 <= self.start_time.hour < 18 and 9 <= self.end_time.hour <= 18):
            raise ValidationError("Appointment must be within working hours (9am–6pm).")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
