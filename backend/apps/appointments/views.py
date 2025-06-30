from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone

from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer
from .utils import (
    send_appointment_reminder,
    export_appointments_csv,
    get_most_booked_mentors,  # ✅ fixed name
    get_busiest_days,
)


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage appointments for mentors and students.
    """
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['start_time', 'end_time', 'status']
    ordering = ['-start_time']
    search_fields = ['mentor__user__username', 'student__username']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AppointmentCreateSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(
            Q(student=user) | Q(mentor__user=user)
        ).order_by('-start_time')

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=["post"])
    def send_reminder(self, request, pk=None):
        """
        Trigger an email reminder for the appointment.
        """
        appointment = self.get_object()
        send_appointment_reminder(appointment)
        return Response({"detail": "Reminder sent successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def export(self, request):
        """
        Export all appointments (for the user) to a CSV file.
        """
        qs = self.get_queryset()
        return export_appointments_csv(qs)

    @action(detail=False, methods=["get"])
    def top_mentors(self, request):
        """
        Show mentors with the most appointments.
        """
        top = get_most_booked_mentors()
        data = [
            {"mentor": m.user.username, "appointments": m.num_appointments}
            for m in top
        ]
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def busiest_days(self, request):
        """
        Return days with the most appointments.
        """
        data = get_busiest_days()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def today(self, request):
        """
        List today’s appointments for the logged-in user.
        """
        now = timezone.now()
        today_qs = self.get_queryset().filter(start_time__date=now.date())
        serializer = self.get_serializer(today_qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        """
        Get future appointments for user.
        """
        upcoming = self.get_queryset().filter(start_time__gte=timezone.now())
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def past(self, request):
        """
        Get past appointments for user.
        """
        past = self.get_queryset().filter(end_time__lt=timezone.now())
        serializer = self.get_serializer(past, many=True)
        return Response(serializer.data)
