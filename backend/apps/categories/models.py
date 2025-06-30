from django.db import models

class CategoryQuerySet(models.QuerySet):
    def by_type(self, category_type):
        return self.filter(type=category_type)

    def top_categories(self, limit=5):
        # Return categories with the most courses
        from apps.courses.models import Course
        return (
            self
            .annotate(course_count=models.Count('courses'))
            .order_by('-course_count')[:limit]
        )

class Category(models.Model):
    TYPE_PHYSICAL     = "Physical"
    TYPE_EDUCATION    = "Education"
    TYPE_PROFESSIONAL = "Professional"
    TYPE_GUIDANCE     = "Guidance"

    TYPE_CHOICES = [
        (TYPE_PHYSICAL,     "Physical & Creative"),
        (TYPE_EDUCATION,    "Education"),
        (TYPE_PROFESSIONAL, "Professional Skills"),
        (TYPE_GUIDANCE,     "Guidance"),
    ]

    name        = models.CharField(max_length=100, unique=True)
    type        = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        ordering = ["type", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def top_courses(self, limit=5):
        from apps.courses.models import Course
        return (
            Course.objects
            .filter(category=self)
            .order_by('-price')[:limit]
        )
