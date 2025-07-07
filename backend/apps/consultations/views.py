from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Consultation
from .serializers import ConsultationSerializer
from services.twilio_client import create_twilio_room, end_twilio_room


class ConsultationViewSet(viewsets.ModelViewSet):
    """
    Manages video consultations between students and mentors.
    Supports:
    - Auto-room creation via Twilio
    - Actions: start, complete, cancel, join-check
    - Role-based access to consultations
    """
    queryset = Consultation.objects.select_related("student", "mentor__user").all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(Q(student=user) | Q(mentor__user=user))

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        """
        🔹 POST /consultations/{id}/start/
        Starts the consultation and provisions a Twilio room.
        """
        consultation = self.get_object()
        if consultation.status != Consultation.STATUS_SCHEDULED:
            return Response(
                {"error": "Consultation is not in a schedulable state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            sid = create_twilio_room(f"consultation-{consultation.pk}")
            consultation.start(twilio_sid=sid)
        except Exception as e:
            return Response(
                {"error": f"Failed to start Twilio room: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"room_sid": sid, "status": "started"})

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """
        🔹 POST /consultations/{id}/complete/
        Marks consultation as completed, ends Twilio room.
        """
        consultation = self.get_object()
        if consultation.status != Consultation.STATUS_IN_PROGRESS:
            return Response(
                {"error": "Only in-progress consultations can be completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            consultation.complete()
            if consultation.twilio_room_sid:
                end_twilio_room(consultation.twilio_room_sid)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"status": "completed"})

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        🔹 POST /consultations/{id}/cancel/
        Cancels the consultation unless already completed/cancelled.
        """
        consultation = self.get_object()
        if consultation.status in [Consultation.STATUS_COMPLETED, Consultation.STATUS_CANCELLED]:
            return Response(
                {"error": "Consultation cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        consultation.cancel()
        return Response({"status": "cancelled"})

    @action(detail=True, methods=["get"])
    def can_join(self, request, pk=None):
        """
        🔹 GET /consultations/{id}/can_join/
        Checks if the current user can join now.
        """
        consultation = self.get_object()
        return Response({"can_join": consultation.can_join(request.user)})

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        """
        🔹 GET /consultations/upcoming/
        Lists upcoming consultations for current user.
        """
        user = request.user
        now = timezone.now()
        consultations = self.get_queryset().filter(
            status=Consultation.STATUS_SCHEDULED,
            scheduled_time__gte=now
        )
        serializer = self.get_serializer(consultations, many=True)
        return Response(serializer.data)
