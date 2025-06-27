from rest_framework import viewsets
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
    - /api/match/mentors/?limit=5
    - /api/match/courses/?limit=5

    Returns a personalized list of mentors or courses based on user profile.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='mentors')
    def mentors(self, request):
        """
        GET /api/match/mentors/?limit=5

        Returns recommended mentors for the logged-in student.
        """
        try:
            limit = int(request.query_params.get('limit', 5))
        except ValueError:
            return Response({"error": "Invalid limit"}, status=400)

        student = request.user
        mentors = recommend_mentors_for_student(student, limit=limit)
        data = MentorRecommendationSerializer(mentors, many=True).data
        return Response(data)

    @action(detail=False, methods=['get'], url_path='courses')
    def courses(self, request):
        """
        GET /api/match/courses/?limit=5

        Returns recommended courses for the logged-in student.
        """
        try:
            limit = int(request.query_params.get('limit', 5))
        except ValueError:
            return Response({"error": "Invalid limit"}, status=400)

        student = request.user
        courses = recommend_courses_for_student(student, limit=limit)
        data = CourseRecommendationSerializer(courses, many=True).data
        return Response(data)
