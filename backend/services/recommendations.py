# onego/backend/services/recommendations.py

from django.db.models import Count, Avg
from apps.courses.models import Course
from apps.mentors.models import MentorProfile
from apps.enrollments.models import Enrollment

def recommend_courses_for_student(student, limit=10):
    """
    Recommend courses for a student based on:
    - Previous enrollments (same categories)
    - Exclude already enrolled courses
    - Popularity by enrollments
    - Fallback to high-price or top-rated
    """
    enrolled_ids = Enrollment.objects.filter(student=student).values_list("course_id", flat=True)
    enrolled_categories = (
        Course.objects.filter(id__in=enrolled_ids)
        .values_list("category_id", flat=True)
        .distinct()
    )

    qs = Course.objects.exclude(id__in=enrolled_ids)
    if enrolled_categories:
        qs = qs.filter(category_id__in=enrolled_categories)

    qs = qs.annotate(num_enrolls=Count("enrollments"))
    results = list(qs.order_by("-num_enrolls")[:limit])

    if len(results) < limit:
        extras = Course.objects.exclude(id__in=[c.id for c in results + list(Course.objects.filter(id__in=enrolled_ids))])
        extras = extras.order_by("-price")[: (limit - len(results))]
        results += list(extras)

    return results

def recommend_mentors_for_student(student, limit=10):
    """
    Recommend mentors for a student based on:
    - Matching categories from previously enrolled courses
    - Mentor rating and popularity (course count)
    """
    enrolled_ids = Enrollment.objects.filter(student=student).values_list("course_id", flat=True)
    category_ids = (
        Course.objects.filter(id__in=enrolled_ids)
        .values_list("category_id", flat=True)
        .distinct()
    )

    qs = MentorProfile.objects.all()
    if category_ids:
        qs = qs.filter(categories__in=category_ids).distinct()

    qs = qs.annotate(
        popularity_score=Avg("rating") + Count("courses") * 0.1
    ).order_by("-popularity_score")[:limit]

    return list(qs)
