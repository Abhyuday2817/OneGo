from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Avg, Count

from apps.courses.models import Course


class EnrollmentQuerySet(models.QuerySet):
    def by_student(self, student):
        return self.filter(student=student)

    def by_course(self, course):
        return self.filter(course=course)

    def active(self):
        return self.filter(completed=False)

    def completed(self):
        return self.filter(completed=True)

    def with_progress_above(self, percent):
        return [e for e in self if e.progress_percent >= percent]

    def stats_by_course(self):
        return self.values("course__title").annotate(
            total=Count("id"),
            completed=Count("id", filter=Q(completed=True)),
            avg_progress=Avg("progress__progress")
        )


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.JSONField(default=dict, blank=True)
    completed = models.BooleanField(default=False)

    objects = EnrollmentQuerySet.as_manager()

    class Meta:
        unique_together = [["student", "course"]]
        ordering = ["-enrolled_at"]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"

    # ─── PROPERTIES ─────────────────────────────────────────────────────
    @property
    def progress_percent(self):
        if not self.progress:
            return 0
        values = [v for v in self.progress.values() if isinstance(v, (int, float))]
        return round(sum(values) / len(values), 1) if values else 0

    @property
    def modules_remaining(self):
        return len([m for m, pct in self.progress.items() if pct < 100])

    @property
    def days_since_enrollment(self):
        return (timezone.now() - self.enrolled_at).days

    @property
    def is_active(self):
        return not self.completed

    @property
    def module_count(self):
        return len(self.progress)

    # ─── METHODS ─────────────────────────────────────────────────────────
    def time_since_enroll(self):
        return timezone.now() - self.enrolled_at

    def mark_complete(self):
        self.completed = True
        self.progress = {k: 100 for k in self.progress.keys()}
        self.save()

    def update_progress(self, module_name: str, percent: float):
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100")
        self.progress[module_name] = percent
        self.completed = all(p == 100 for p in self.progress.values())
        self.save()

    def reset_progress(self):
        self.progress = {k: 0 for k in self.progress.keys()}
        self.completed = False
        self.save()

    def summary(self):
        return {
            "student": self.student.username,
            "course": self.course.title,
            "progress_percent": self.progress_percent,
            "modules_remaining": self.modules_remaining,
            "days_enrolled": self.days_since_enrollment,
            "completed": self.completed,
        }
