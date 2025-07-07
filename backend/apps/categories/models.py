from django.db import models


class CategoryQuerySet(models.QuerySet):
    def by_type(self, category_type):
        return self.filter(type=category_type)

    def top_categories(self, limit=5):
        """
        Return categories with the most associated courses.
        """
        from apps.courses.models import Course
        return (
            self.annotate(course_count=models.Count('courses'))
            .order_by('-course_count')[:limit]
        )

    def search(self, keyword):
        """
        Search categories by name or description.
        """
        return self.filter(
            models.Q(name__icontains=keyword) | models.Q(description__icontains=keyword)
        )


class Category(models.Model):
    TYPE_PHYSICAL     = "Physical"
    TYPE_EDUCATION    = "Education"
    TYPE_PROFESSIONAL = "Professional"
    TYPE_GUIDANCE     = "Guidance"

    TYPE_CHOICES = [
        (TYPE_PHYSICAL, "Physical & Creative"),
        (TYPE_EDUCATION, "Education"),
        (TYPE_PROFESSIONAL, "Professional Skills"),
        (TYPE_GUIDANCE, "Guidance"),
    ]

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        ordering = ["type", "name"]
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def top_courses(self, limit=5):
        """
        Return the most expensive top N courses in this category.
        """
        from apps.courses.models import Course
        return (
            Course.objects
            .filter(category=self)
            .order_by('-price')[:limit]
        )

    def total_courses(self):
        """
        Count total courses in this category.
        """
        return self.courses.count()

    def average_price(self):
        """
        Average price of courses in this category.
        """
        from apps.courses.models import Course
        return (
            Course.objects.filter(category=self)
            .aggregate(avg=models.Avg("price"))["avg"] or 0
        )

    def has_free_courses(self):
        """
        Check if any course in this category is free.
        """
        from apps.courses.models import Course
        return Course.objects.filter(category=self, price=0).exists()

    def related_mentors(self, limit=5):
        """
        Return mentors who have expertise in this category.
        """
        from apps.mentors.models import MentorProfile
        return (
            MentorProfile.objects
            .filter(specialties=self)
            .order_by('-rating')[:limit]
        )
