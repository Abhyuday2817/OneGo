from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend
from .models import Enrollment
from .serializers import EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    list / retrieve / create / update / destroy enrollments.
    Includes progress tracking, completion marking, and analytics.
    """
    queryset = Enrollment.objects.select_related("student", "course").all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'course']
    search_fields = ['course__title', 'student__username']
    ordering_fields = ['enrolled_at', 'completed']
    ordering = ['-enrolled_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.by_student(user)

    def perform_create(self, serializer):
        # Associate the logged-in student
        serializer.save(student=self.request.user)

    @action(detail=True, methods=["post"], url_path="mark-complete")
    def mark_complete(self, request, pk=None):
        """
        POST /api/enrollments/{id}/mark-complete/
        Marks all progress modules as complete (100%).
        """
        enrollment = self.get_object()
        enrollment.mark_complete()
        return Response(self.get_serializer(enrollment).data)

    @action(detail=True, methods=["post"], url_path="update-progress")
    def update_progress(self, request, pk=None):
        """
        POST /api/enrollments/{id}/update-progress/
        Body: { "module": "chapter1", "percent": 80 }
        """
        enrollment = self.get_object()
        module = request.data.get("module")
        percent = request.data.get("percent")

        if not module or percent is None:
            return Response(
                {"error": "Both 'module' and 'percent' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            percent = float(percent)
            enrollment.update_progress(module, percent)
        except ValueError:
            return Response(
                {"error": "Percent must be a valid number."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(self.get_serializer(enrollment).data)

    @action(detail=False, methods=["get"], url_path="analytics", permission_classes=[IsAdminUser])
    def analytics(self, request):
        """
        Admin-only: Shows completion stats across all enrollments.
        GET /api/enrollments/analytics/
        """
        total = Enrollment.objects.count()
        completed = Enrollment.objects.filter(completed=True).count()
        percent = (completed / total * 100) if total > 0 else 0

        return Response({
            "total_enrollments": total,
            "completed": completed,
            "completion_rate": round(percent, 2)
        })
