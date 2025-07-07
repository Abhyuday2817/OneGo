from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils.text import slugify
from apps.mentors.models import MentorProfile
from apps.categories.models import Category

import itertools


class CourseManager(models.Manager):
    def live(self):
        return self.filter(delivery_type=Course.DELIVERY_LIVE)

    def recorded(self):
        return self.filter(delivery_type=Course.DELIVERY_RECORDED)

    def by_category(self, category_id):
        return self.filter(category_id=category_id)

    def trending(self):
        return self.order_by('-enrollments_count')[:10]


class Course(models.Model):
    DELIVERY_LIVE = "Live"
    DELIVERY_RECORDED = "Recorded"
    DELIVERY_GROUP = "Group"
    DELIVERY_PROJECT = "Project"

    DELIVERY_CHOICES = [
        (DELIVERY_LIVE, "Live 1:1"),
        (DELIVERY_RECORDED, "Recorded"),
        (DELIVERY_GROUP, "Group Class"),
        (DELIVERY_PROJECT, "Short-term Project"),
    ]

    # Basic Info
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    # Relations
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name="courses")

    # Pricing & Delivery
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    duration_hours = models.PositiveIntegerField(null=True, blank=True)
    schedule_info = models.JSONField(default=dict, blank=True, help_text="e.g. {'slots': ['Mon 5pm', 'Wed 7pm']}")

    # Media
    preview_video = models.URLField(blank=True, null=True)
    intro_pdf = models.FileField(upload_to='courses/pdfs/', blank=True, null=True)

    # Advanced options
    certificate_available = models.BooleanField(default=False)
    enrollment_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Max students allowed")
    published = models.BooleanField(default=True)

    # Stats
    enrollments_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CourseManager()

    class Meta:
        ordering = ['-created_at']
        unique_together = [['title', 'mentor']]
        indexes = [models.Index(fields=['slug'])]
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.title} by {self.mentor.user.username}"

    def related(self, limit=5):
        return Course.objects.filter(category=self.category).exclude(pk=self.pk).order_by('-price')[:limit]

    def enroll(self, student):
        from apps.enrollments.models import Enrollment
        return Enrollment.objects.create(course=self, student=student)

    def update_rating(self):
        from apps.mentorship_reviews.models import MentorReview
        ratings = MentorReview.objects.filter(mentor=self.mentor).aggregate(avg=models.Avg('rating'))
        self.rating = round(ratings['avg'] or 0, 2)
        self.save()

    def is_full(self):
        from apps.enrollments.models import Enrollment
        if self.enrollment_limit:
            return Enrollment.objects.filter(course=self).count() >= self.enrollment_limit
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title or "course")
            slug = base_slug
            for i in itertools.count(1):
                if not Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    break
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)
