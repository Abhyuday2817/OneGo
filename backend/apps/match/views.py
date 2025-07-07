from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    MentorRecommendationSerializer,
    CourseRecommendationSerializer,
)
from services.recommendations import (
    recommend_mentors_for_student,
    recommend_courses_for_student,
)


class MatchViewSet(viewsets.ViewSet):
    """
    Recommendation API:
    - GET /api/match/mentors/?limit=5
    - GET /api/match/courses/?limit=5

    Returns a personalized list of mentors or courses based on user profile.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='mentors')
    def mentors(self, request):
        """
        Returns recommended mentors for the logged-in student.
        """
        try:
            limit = int(request.query_params.get('limit', 5))
        except ValueError:
            return Response({"error": "Invalid limit"}, status=status.HTTP_400_BAD_REQUEST)

        student = request.user
        try:
            mentors = recommend_mentors_for_student(student, limit=limit)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = MentorRecommendationSerializer(mentors, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='courses')
    def courses(self, request):
        """
        Returns recommended courses for the logged-in student.
        """
        try:
            limit = int(request.query_params.get('limit', 5))
        except ValueError:
            return Response({"error": "Invalid limit"}, status=status.HTTP_400_BAD_REQUEST)

        student = request.user
        try:
            courses = recommend_courses_for_student(student, limit=limit)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = CourseRecommendationSerializer(courses, many=True).data
        return Response(data, status=status.HTTP_200_OK)
