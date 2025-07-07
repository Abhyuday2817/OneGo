from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Enrollment
from .serializers import EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    📚 Handles all enrollment operations:
    - Students: enroll, view, update progress, mark complete
    - Admins: analytics, filter all enrollments
    """
    queryset = Enrollment.objects.select_related("student", "course").all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'course', 'student']
    search_fields = ['course__title', 'student__username']
    ordering_fields = ['enrolled_at', 'completed']
    ordering = ['-enrolled_at']

    def get_queryset(self):
        """
        Restrict students to only their enrollments.
        Admins see all.
        """
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.by_student(user)

    def perform_create(self, serializer):
        """
        Auto-assign logged-in user as student if not explicitly passed.
        """
        if not serializer.validated_data.get("student"):
            serializer.save(student=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=["post"], url_path="mark-complete")
    def mark_complete(self, request, pk=None):
        """
        ✅ POST /api/enrollments/{id}/mark-complete/
        Marks this enrollment as completed and sets 100% progress.
        """
        enrollment = self.get_object()
        enrollment.mark_complete()
        return Response(self.get_serializer(enrollment).data)

    @action(detail=True, methods=["post"], url_path="update-progress")
    def update_progress(self, request, pk=None):
        """
        ✅ POST /api/enrollments/{id}/update-progress/
        Body: { "module": "Intro", "percent": 75 }
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
            if not (0 <= percent <= 100):
                raise ValueError()
            enrollment.update_progress(module, percent)
        except ValueError:
            return Response({"error": "Percent must be a number between 0 and 100."}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response(self.get_serializer(enrollment).data)

    @action(detail=False, methods=["get"], url_path="analytics", permission_classes=[IsAdminUser])
    def analytics(self, request):
        """
        📊 GET /api/enrollments/analytics/
        Returns overall enrollment stats.
        """
        total = Enrollment.objects.count()
        completed = Enrollment.objects.completed().count()
        percent = (completed / total * 100) if total else 0

        return Response({
            "total_enrollments": total,
            "completed": completed,
            "completion_rate": round(percent, 2)
        })

    @action(detail=False, methods=["get"], url_path="recent-completions", permission_classes=[IsAdminUser])
    def recent_completions(self, request):
        """
        🕒 GET /api/enrollments/recent-completions/
        Returns last 10 completed enrollments.
        """
        recent = Enrollment.objects.completed().order_by("-enrolled_at")[:10]
        return Response(self.get_serializer(recent, many=True).data)
