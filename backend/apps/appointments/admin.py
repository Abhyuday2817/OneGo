# apps/appointments/admin.py

from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin interface for student-mentor appointments."""
    list_display = (
        'id',
        'student',
        'mentor',
        'start_time',
        'end_time',
        'status',
        'duration_minutes',
        'created_at',
    )
    list_filter = (
        'status',
        'start_time',
        'mentor',
    )
    search_fields = (
        'student__username',
        'mentor__user__username',
        'notes',
    )
    ordering = ('-start_time',)
    readonly_fields = ('created_at', 'duration_minutes')

    def duration_minutes(self, obj):
        if obj.start_time and obj.end_time:
            duration = obj.end_time - obj.start_time
            return int(duration.total_seconds() // 60)
        return "-"
    duration_minutes.short_description = "Duration (mins)"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'mentor__user')
