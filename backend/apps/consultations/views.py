from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Consultation
from .serializers import ConsultationSerializer
from services.twilio_client import create_twilio_room, end_twilio_room


class ConsultationViewSet(viewsets.ModelViewSet):
    """
    Manages video call consultations (booked between students and mentors).
    Includes start, complete, and cancel operations.
    """
    queryset = Consultation.objects.select_related("student", "mentor__user").all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(
            Q(student=user) | Q(mentor__user=user)
        )

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        """
        Start a consultation (provisions Twilio room if required).
        """
        consultation = self.get_object()
        if consultation.status != Consultation.STATUS_SCHEDULED:
            return Response(
                {"error": "Consultation is not in a schedulable state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sid = create_twilio_room(consultation.twilio_room_sid or f"consultation-{consultation.pk}")
        consultation.twilio_room_sid = sid
        consultation.status = Consultation.STATUS_IN_PROGRESS
        consultation.save()
        return Response({"room_sid": sid, "status": "started"})

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """
        Mark a consultation as completed and end the Twilio room.
        """
        consultation = self.get_object()
        if consultation.status != Consultation.STATUS_IN_PROGRESS:
            return Response(
                {"error": "Only in-progress consultations can be completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        consultation.status = Consultation.STATUS_COMPLETED
        consultation.save()

        if consultation.twilio_room_sid:
            end_twilio_room(consultation.twilio_room_sid)

        return Response({"status": "completed"})

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        Cancel a consultation if it hasn't been completed or already cancelled.
        """
        consultation = self.get_object()
        if consultation.status in [Consultation.STATUS_COMPLETED, Consultation.STATUS_CANCELLED]:
            return Response(
                {"error": "Consultation cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        consultation.status = Consultation.STATUS_CANCELLED
        consultation.save()
        return Response({"status": "cancelled"})
