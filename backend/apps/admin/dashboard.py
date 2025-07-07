### 📁 apps/admin/dashboard.py

from django.db.models import Sum, Count, Avg
from django.utils import timezone
from payments.models import Payment
from enrollments.models import Enrollment
from sessions.models import Session
from categories.models import Category
from mentors.models import MentorProfile


def total_revenue(start=None, end=None):
    """
    Sum of all completed payments in [start, end].
    """
    qs = Payment.objects.filter(status=Payment.STATUS_COMPLETED)
    if start:
        qs = qs.filter(created_at__gte=start)
    if end:
        qs = qs.filter(created_at__lte=end)
    return qs.aggregate(total=Sum("amount"))['total'] or 0


def revenue_by_month(year=None):
    """
    Returns a dict mapping month (1–12) to total revenue in that month.
    """
    now = timezone.now()
    if year is None:
        year = now.year
    data = (
        Payment.objects.filter(
            status=Payment.STATUS_COMPLETED,
            created_at__year=year
        )
        .annotate(month=timezone.functions.ExtractMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )
    return {item["month"]: item["total"] for item in data}


def top_categories_by_enrollment(limit=5):
    """
    Returns the top `limit` categories ordered by number of enrollments.
    """
    data = (
        Enrollment.objects
        .values("course__category__id", "course__category__name")
        .annotate(count=Count("id"))
        .order_by("-count")[:limit]
    )
    return [
        {"id": d["course__category__id"], "name": d["course__category__name"], "enrollments": d["count"]}
        for d in data
    ]


def top_mentors_by_sessions(limit=5):
    """
    Returns the top `limit` mentors ordered by number of completed sessions.
    """
    data = (
        Session.objects.filter(status=Session.STATUS_COMPLETED)
        .values("mentor__id", "mentor__user__username")
        .annotate(count=Count("id"), avg_rating=Avg("mentor__rating"))
        .order_by("-count")[:limit]
    )
    return [
        {
            "mentor_id": d["mentor__id"],
            "username": d["mentor__user__username"],
            "sessions_completed": d["count"],
            "avg_rating": round(d["avg_rating"] or 0, 2),
        }
        for d in data
    ]


def mentor_performance(mentor_id):
    """
    Returns detailed performance metrics for a single mentor.
    """
    mentor = MentorProfile.objects.get(pk=mentor_id)
    total_sessions = Session.objects.filter(
        mentor=mentor, status=Session.STATUS_COMPLETED
    ).count()
    avg_rating = mentor.rating or 0
    revenue = (
        Payment.objects.filter(
            status=Payment.STATUS_COMPLETED,
            user=mentor.user,
            method__icontains="session"
        )
        .aggregate(total=Sum("amount"))['total'] or 0
    )
    return {
        "mentor": mentor.user.username,
        "total_sessions": total_sessions,
        "average_rating": round(avg_rating, 2),
        "total_revenue": revenue,
    }


def student_overview(student_id):
    """
    Returns total sessions attended, enrolled courses, and progress for a student.
    """
    from users.models import User
    student = User.objects.get(pk=student_id)
    sessions = Session.objects.filter(student=student, status=Session.STATUS_COMPLETED).count()
    enrollments = Enrollment.objects.filter(student=student).count()
    progress = Enrollment.objects.filter(student=student).aggregate(avg_progress=Avg('progress'))['avg_progress'] or 0.0
    return {
        "student": student.username,
        "sessions_attended": sessions,
        "enrolled_courses": enrollments,
        "average_progress": round(progress, 2),
    }