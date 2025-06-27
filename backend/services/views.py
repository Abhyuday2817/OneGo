from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.mentors.models import MentorProfile
from apps.mentors.serializers import MentorProfileSerializer
from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer
from services.recommendations import (
    recommend_mentors_for_student,
    recommend_courses_for_student,
)


class MatchViewSet(viewsets.ViewSet):
    """
    /api/match/mentors/  → personalized mentor recommendations
    /api/match/courses/  → personalized course recommendations
    """

    @action(detail=False, methods=["get"])
    def mentors(self, request):
        """
        Return a list of up to `limit` mentors recommended for the current user.
        Accepts `?limit=N` query parameter (default 5).
        """
        limit = int(request.query_params.get("limit", 5))
        mentors = recommend_mentors_for_student(request.user, limit=limit)
        serializer = MentorProfileSerializer(mentors, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def courses(self, request):
        """
        Return a list of up to `limit` courses recommended for the current user.
        Accepts `?limit=N` query parameter (default 5).
        """
        limit = int(request.query_params.get("limit", 5))
        courses = recommend_courses_for_student(request.user, limit=limit)
        serializer = CourseSerializer(courses, many=True, context={"request": request})
        return Response(serializer.data)
