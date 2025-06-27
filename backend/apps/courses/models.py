from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from apps.mentors.models import MentorProfile
from apps.categories.models import Category

class CourseManager(models.Manager):
    def live(self):
        """All live 1:1 courses."""
        return self.filter(delivery_type=Course.DELIVERY_LIVE)

    def by_category(self, category_id):
        """Courses in a given category."""
        return self.filter(category_id=category_id)


class Course(models.Model):
    DELIVERY_LIVE     = "Live"
    DELIVERY_RECORDED = "Recorded"
    DELIVERY_GROUP    = "Group"
    DELIVERY_PROJECT  = "Project"

    DELIVERY_CHOICES = [
        (DELIVERY_LIVE,     "Live 1:1"),
        (DELIVERY_RECORDED, "Recorded"),
        (DELIVERY_GROUP,    "Group Class"),
        (DELIVERY_PROJECT,  "Short-term Project"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES
    )
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    schedule_info = models.JSONField(
        default=dict,
        blank=True,
        help_text="e.g. {'slots': [...]}"
    )
    duration_hours = models.PositiveIntegerField(
        help_text="Duration of the course in hours",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CourseManager()

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["title", "mentor"]]
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.title} by {self.mentor.user.username}"

    def related(self, limit=5):
        """
        Return up to `limit` other courses in the same category,
        ordered by descending price.
        """
        return (
            Course.objects
            .filter(category=self.category)
            .exclude(pk=self.pk)
            .order_by("-price")[:limit]
        )

    def enroll(self, student):
        """
        Enroll a student in this course.
        Creates an Enrollment record (must exist).
        """
        from apps.enrollments.models import Enrollment
        return Enrollment.objects.create(course=self, student=student)