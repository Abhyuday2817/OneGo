from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.mentors.models import MentorProfile
from services.availability import is_available


class ConsultationQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(
            status=Consultation.STATUS_SCHEDULED,
            scheduled_time__gte=timezone.now()
        )

    def for_user(self, user):
        return self.filter(models.Q(student=user) | models.Q(mentor__user=user))

    def completed(self):
        return self.filter(status=Consultation.STATUS_COMPLETED)

    def in_progress(self):
        return self.filter(status=Consultation.STATUS_IN_PROGRESS)

    def cancelled(self):
        return self.filter(status=Consultation.STATUS_CANCELLED)


class Consultation(models.Model):
    """
    A scheduled video-call consultation (e.g., via Twilio).
    """

    STATUS_SCHEDULED   = "scheduled"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED   = "completed"
    STATUS_CANCELLED   = "cancelled"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED,   "Scheduled"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED,   "Completed"),
        (STATUS_CANCELLED,   "Cancelled"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consultations_as_student"
    )
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        related_name="consultations_as_mentor"
    )
    topic = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scheduled_time = models.DateTimeField()
    duration_mins = models.PositiveIntegerField(help_text="Duration in minutes")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SCHEDULED
    )
    twilio_room_sid = models.CharField(
        max_length=100,
        blank=True,
        help_text="Twilio Room SID once the session is started"
    )
    feedback = models.TextField(blank=True, help_text="Optional feedback after completion")
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="Optional rating out of 5")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ConsultationQuerySet.as_manager()

    class Meta:
        ordering = ["-scheduled_time"]
        indexes = [
            models.Index(fields=["mentor", "scheduled_time"]),
            models.Index(fields=["student", "scheduled_time"]),
        ]
        verbose_name_plural = "Consultations"

    def __str__(self):
        return f"Consultation #{self.pk}: {self.student.username} → {self.mentor.user.username} @ {self.scheduled_time}"

    @property
    def end_time(self):
        return self.scheduled_time + timezone.timedelta(minutes=self.duration_mins)

    def clean(self):
        """
        Validations:
        1. Scheduled time must be in the future.
        2. Student and mentor must be different.
        3. Mentor must be available.
        """
        if self.scheduled_time <= timezone.now():
            raise ValidationError({"scheduled_time": "Must schedule a future time."})

        if self.student == self.mentor.user:
            raise ValidationError("Student and mentor must be different users.")

        if not is_available(self.mentor, self.scheduled_time, self.end_time):
            raise ValidationError("Mentor is not available during this time slot.")

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures clean() runs before saving
        super().save(*args, **kwargs)

    def can_join(self, user) -> bool:
        """
        Joinable 5 minutes before scheduled_time until end_time.
        Only the student or mentor can join.
        """
        now = timezone.now()
        if user not in (self.student, self.mentor.user):
            return False
        if self.status not in (self.STATUS_SCHEDULED, self.STATUS_IN_PROGRESS):
            return False
        return (self.scheduled_time - timezone.timedelta(minutes=5)) <= now <= self.end_time

    def start(self, twilio_sid: str):
        """
        Start consultation and assign Twilio room SID.
        """
        if self.status != self.STATUS_SCHEDULED:
            raise ValidationError("Only scheduled consultations can be started.")
        self.status = self.STATUS_IN_PROGRESS
        self.twilio_room_sid = twilio_sid
        self.save()

    def complete(self, rating=None, feedback=""):
        """
        Complete the consultation. Optionally attach feedback and rating.
        """
        if self.status != self.STATUS_IN_PROGRESS:
            raise ValidationError("Only in-progress consultations can be completed.")
        self.status = self.STATUS_COMPLETED
        self.rating = rating
        self.feedback = feedback
        self.save()

    def cancel(self):
        """
        Cancel the consultation unless already completed.
        """
        if self.status == self.STATUS_COMPLETED:
            raise ValidationError("Cannot cancel a completed consultation.")
        self.status = self.STATUS_CANCELLED
        self.save()

    def is_over(self):
        return timezone.now() > self.end_time

    def duration_display(self):
        return f"{self.duration_mins} mins"

    def student_username(self):
        return self.student.username

    def mentor_username(self):
        return self.mentor.user.username
