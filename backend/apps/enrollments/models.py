# apps/enrollments/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.courses.models import Course  # ✅ Correct import from apps

class EnrollmentQuerySet(models.QuerySet):
    def by_student(self, student):
        return self.filter(student=student)

    def completed(self):
        return self.filter(completed=True)


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

    @property
    def progress_percent(self):
        """Returns average progress percentage across all modules."""
        if not self.progress:
            return 0
        values = [v for v in self.progress.values() if isinstance(v, (int, float))]
        return round(sum(values) / len(values), 1) if values else 0

    @property
    def modules_remaining(self):
        """Counts how many modules are below 100% completion."""
        return len([m for m, pct in self.progress.items() if pct < 100])

    @property
    def days_since_enrollment(self):
        return (timezone.now() - self.enrolled_at).days

    def mark_complete(self):
        """Mark all modules 100% and set enrollment as completed."""
        self.completed = True
        self.progress = {k: 100 for k in self.progress.keys()}
        self.save()

    def update_progress(self, module_name: str, percent: float):
        """Update progress for a specific module."""
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100")
        self.progress[module_name] = percent
        if all(p == 100 for p in self.progress.values()):
            self.completed = True
        self.save()

    def time_since_enroll(self):
        """Returns the full timedelta since enrollment."""
        return timezone.now() - self.enrolled_at
