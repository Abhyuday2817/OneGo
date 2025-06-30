from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as df_filters
from django.shortcuts import get_object_or_404

from .models import Course, CourseQuiz
from .serializers import CourseSerializer, CourseQuizSerializer
from services.recommendations import recommend_courses_for_student


class CourseFilter(df_filters.FilterSet):
    price_min = df_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = df_filters.NumberFilter(field_name="price", lookup_expr="lte")
    delivery  = df_filters.CharFilter(field_name="delivery_type", lookup_expr="iexact")
    category  = df_filters.NumberFilter(field_name="category_id")
    mentor    = df_filters.NumberFilter(field_name="mentor_id")

    class Meta:
        model = Course
        fields = ['category', 'delivery', 'price_min', 'price_max', 'mentor']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('category', 'mentor__user').all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Filtering, searching, ordering
    filterset_class = CourseFilter
    filter_backends = [
        df_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['title', 'description', 'mentor__user__username']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        mentor_profile = self.request.user.mentorprofile
        serializer.save(mentor=mentor_profile)

    @action(detail=True, methods=['post'], url_path='enroll')
    def enroll(self, request, pk=None):
        course = self.get_object()
        student = request.user
        try:
            enrollment = course.enroll(student)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "enrolled",
            "course_id": course.id,
            "student_id": student.id,
            "enrollment_id": enrollment.id
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='related')
    def related(self, request, pk=None):
        course = self.get_object()
        related_courses = course.related(limit=5)

        page = self.paginate_queryset(related_courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(related_courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='match')
    def match(self, request):
        student = request.user
        budget = request.query_params.get('budget')
        delivery = request.query_params.get('delivery')

        try:
            courses = recommend_courses_for_student(student, limit=20)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if budget:
            try:
                max_price = float(budget)
                courses = [c for c in courses if c.price <= max_price]
            except ValueError:
                return Response({"error": "Invalid budget value."}, status=status.HTTP_400_BAD_REQUEST)

        if delivery:
            courses = [c for c in courses if c.delivery_type.lower() == delivery.lower()]

        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)


class CourseQuizViewSet(viewsets.ModelViewSet):
    queryset = CourseQuiz.objects.all()
    serializer_class = CourseQuizSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
