# apps/appointments/views.py

from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone

from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    AppointmentCreateSerializer,
    AppointmentUpdateStatusSerializer,
)
from .utils import (
    send_appointment_reminder,
    export_appointments_csv,
    get_most_booked_mentors,
    get_busiest_days,
)


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    Manage Appointments — Students book, Mentors manage, Admins oversee.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Appointment.objects.select_related("student", "mentor").all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['start_time', 'end_time', 'status']
    ordering = ['-start_time']
    search_fields = ['mentor__user__username', 'student__username']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AppointmentCreateSerializer
        if self.action == "update_status":
            return AppointmentUpdateStatusSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(
            Q(student=user) | Q(mentor__user=user)
        ).order_by('-start_time')

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    # 🔔 Send Reminder
    @action(detail=True, methods=["post"])
    def send_reminder(self, request, pk=None):
        appointment = self.get_object()
        send_appointment_reminder(appointment)
        return Response({"detail": "Reminder sent."}, status=status.HTTP_200_OK)

    # 📥 Export CSV
    @action(detail=False, methods=["get"])
    def export(self, request):
        return export_appointments_csv(self.get_queryset())

    # 🏆 Top mentors
    @action(detail=False, methods=["get"])
    def top_mentors(self, request):
        top = get_most_booked_mentors()
        return Response([
            {"mentor": m.user.username, "appointments": m.num_appointments}
            for m in top
        ])

    # 📈 Busiest days
    @action(detail=False, methods=["get"])
    def busiest_days(self, request):
        return Response(get_busiest_days())

    # 🗓️ Today's appointments
    @action(detail=False, methods=["get"])
    def today(self, request):
        today_qs = self.get_queryset().filter(start_time__date=timezone.now().date())
        serializer = self.get_serializer(today_qs, many=True)
        return Response(serializer.data)

    # ⏳ Upcoming
    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        future = self.get_queryset().filter(start_time__gte=timezone.now())
        serializer = self.get_serializer(future, many=True)
        return Response(serializer.data)

    # ⏱️ Past
    @action(detail=False, methods=["get"])
    def past(self, request):
        past = self.get_queryset().filter(end_time__lt=timezone.now())
        serializer = self.get_serializer(past, many=True)
        return Response(serializer.data)

    # ❌ Cancel (Student Only)
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        if request.user != appointment.student:
            return Response({"error": "Only the student can cancel."}, status=403)
        if appointment.end_time < timezone.now():
            return Response({"error": "Cannot cancel past appointments."}, status=400)
        appointment.status = "canceled"
        appointment.save()
        return Response({"status": "Cancelled"}, status=200)

    # ✅ Mark Completed (Mentor)
    @action(detail=True, methods=["post"])
    def mark_completed(self, request, pk=None):
        appointment = self.get_object()
        if request.user != appointment.mentor.user:
            return Response({"error": "Only mentor can mark as completed."}, status=403)
        if appointment.status != "confirmed":
            return Response({"error": "Only confirmed appointments can be completed."}, status=400)
        appointment.status = "completed"
        appointment.save()
        return Response({"status": "Marked as completed"}, status=200)

    # ⚙️ Admin Only: Manually Update Status
    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"error": "Admin only"}, status=403)
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Updated"})
        return Response(serializer.errors, status=400)
