from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from icalendar import Calendar, Event


class SessionQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(start_time__gt=timezone.now())

    def past(self):
        return self.filter(end_time__lt=timezone.now())

    def by_student(self, student):
        return self.filter(student=student)

    def by_mentor(self, mentor):
        return self.filter(mentor=mentor)

    def conflicts_for(self, mentor, start, end):
        return self.filter(
            mentor=mentor,
            start_time__lt=end,
            end_time__gt=start,
            status__in=[
                Session.STATUS_SCHEDULED,
                Session.STATUS_ONGOING,
            ],
        )


class Session(models.Model):
    # Session Types
    TYPE_LIVE = "Live"
    TYPE_PAY_PER_MIN = "PayPerMinute"
    TYPE_FIXED = "Fixed"

    TYPE_CHOICES = [
        (TYPE_LIVE, "Live"),
        (TYPE_PAY_PER_MIN, "Pay-per-minute"),
        (TYPE_FIXED, "Fixed-rate"),
    ]

    # Status Choices
    STATUS_SCHEDULED = "Scheduled"
    STATUS_ONGOING = "Ongoing"
    STATUS_COMPLETED = "Completed"
    STATUS_CANCELLED = "Cancelled"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions_as_student"
    )

    mentor = models.ForeignKey(
        "mentors.MentorProfile",
        on_delete=models.CASCADE,
        related_name="sessions_as_mentor"
    )

    session_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    rate_applied = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    student_confirmed = models.BooleanField(default=False)
    mentor_confirmed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    objects = SessionQuerySet.as_manager()

    class Meta:
        ordering = ["-start_time"]
        unique_together = [["mentor", "start_time", "end_time"]]
        indexes = [
            models.Index(fields=["mentor", "start_time"]),
            models.Index(fields=["student", "start_time"]),
        ]

    def __str__(self):
        return (
            f"{self.get_session_type_display()} session "
            f"{self.student.username} ↔ {self.mentor.user.username} "
            f"on {self.start_time:%Y-%m-%d %H:%M}"
        )

    def duration_minutes_calc(self):
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() // 60)

    def total_cost(self):
        if self.session_type == self.TYPE_PAY_PER_MIN:
            return self.duration_minutes_calc() * float(self.rate_applied)
        return float(self.rate_applied)

    def complete(self):
        self.status = self.STATUS_COMPLETED
        self.save()

    def cancel(self):
        self.status = self.STATUS_CANCELLED
        self.save()

    def try_verify(self):
        if not self.verified and self.student_confirmed and self.mentor_confirmed:
            self.verified = True
            self.save()

    def start_session(self):
        self.actual_start_time = timezone.now()
        self.status = self.STATUS_ONGOING
        self.save()

    def end_session(self):
        self.actual_end_time = timezone.now()
        if self.actual_start_time:
            duration = (self.actual_end_time - self.actual_start_time).total_seconds() / 60
            self.duration_minutes = round(duration)
            self.total_price = self.duration_minutes * float(self.rate_applied)
        self.status = self.STATUS_COMPLETED
        self.save()

    def to_ical_event(self) -> Event:
        ev = Event()
        ev.add("uid", f"session-{self.pk}@onego.example.com")
        ev.add("dtstamp", timezone.now())
        ev.add("dtstart", self.start_time)
        ev.add("dtend", self.end_time)
        summary = f"{self.student.username} ↔ {self.mentor.user.username}"
        ev.add("summary", summary)
        ev.add("description", f"{self.get_session_type_display()} session")
        return ev

    @classmethod
    def export_ical_for_user(cls, user) -> str:
        cal = Calendar()
        cal.add("prodid", "-//OneGo Sessions Export//example.com//")
        cal.add("version", "2.0")
        qs = cls.objects.filter(
            models.Q(student=user) | models.Q(mentor__user=user),
            start_time__gt=timezone.now()
        )
        for session in qs:
            cal.add_component(session.to_ical_event())
        return cal.to_ical().decode("utf-8")
