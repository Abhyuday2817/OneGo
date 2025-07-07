from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Avg

from apps.courses.models import Course
from apps.sessions.models import Session
from apps.reviews.models import Review
from apps.wallets.models import Wallet
from apps.mentors.models import MentorProfile
from apps.users.models import StudentProfile

class MentorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            mentor_profile = MentorProfile.objects.get(user=request.user)

            courses = Course.objects.filter(mentor=mentor_profile)
            sessions = Session.objects.filter(mentor=mentor_profile)
            # Use mentor_profile as reviewee if Review.reviewee is FK to MentorProfile
            if Review._meta.get_field('reviewee').related_model == MentorProfile:
                reviews = Review.objects.filter(reviewee=mentor_profile)
            else:
                # fallback: assume reviewee is user
                reviews = Review.objects.filter(reviewee=request.user)
            wallet = Wallet.objects.filter(user=request.user).first()

            average_rating = reviews.aggregate(avg=Avg("rating"))["avg"] or 0.0

            # Check for badges only if the field exists
            badges = []
            if hasattr(mentor_profile, "badges"):
                badges_qs = getattr(mentor_profile, "badges")
                if hasattr(badges_qs, "values_list"):
                    badges = list(badges_qs.values_list("title", flat=True))

            data = {
                "mentor_name": request.user.get_full_name() or request.user.username,
                "total_courses": courses.count(),
                "total_sessions": sessions.count(),
                "average_rating": round(average_rating, 2),
                "earnings": float(wallet.balance) if wallet and hasattr(wallet, "balance") else 0.0,
                "badges": badges,
            }
            return Response(data, status=status.HTTP_200_OK)

        except MentorProfile.DoesNotExist:
            return Response({"detail": "Mentor profile not found."}, status=status.HTTP_404_NOT_FOUND)

class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student_profile = StudentProfile.objects.get(user=request.user)

            enrolled_courses = Course.objects.filter(enrollments__student=request.user)
            sessions = Session.objects.filter(student=request.user)
            reviews = Review.objects.filter(reviewer=request.user)

            # Check for badges only if the field exists
            badges = []
            if hasattr(student_profile, "badges"):
                badges_qs = getattr(student_profile, "badges")
                if hasattr(badges_qs, "values_list"):
                    badges = list(badges_qs.values_list("title", flat=True))

            data = {
                "student_name": request.user.get_full_name() or request.user.username,
                "enrolled_courses": enrolled_courses.count(),
                "total_sessions": sessions.count(),
                "given_reviews": reviews.count(),
                "badges": badges,
            }
            return Response(data, status=status.HTTP_200_OK)

        except StudentProfile.DoesNotExist:
            return Response({"detail": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)