from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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
            courses = Course.objects.filter(mentor=request.user)
            sessions = Session.objects.filter(mentor=request.user)
            reviews = Review.objects.filter(mentor=request.user)
            wallet = Wallet.objects.get(user=request.user)

            data = {
                "mentor_name": mentor_profile.full_name,
                "total_courses": courses.count(),
                "total_sessions": sessions.count(),
                "average_rating": reviews.aggregate_avg_rating() if hasattr(reviews, 'aggregate_avg_rating') else None,
                "earnings": wallet.balance,
                "badges": list(mentor_profile.badges.values_list('title', flat=True)) if hasattr(mentor_profile, 'badges') else [],
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
            reviews = Review.objects.filter(student=request.user)

            data = {
                "student_name": student_profile.full_name,
                "enrolled_courses": enrolled_courses.count(),
                "total_sessions": sessions.count(),
                "given_reviews": reviews.count(),
                "badges": list(student_profile.badges.values_list('title', flat=True)) if hasattr(student_profile, 'badges') else [],
            }
            return Response(data, status=status.HTTP_200_OK)
        except StudentProfile.DoesNotExist:
            return Response({"detail": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
