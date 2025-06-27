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
    )
    list_filter = (
        'status',
        'start_time',
    )
    search_fields = (
        'student__username',
        'mentor__user__username',
    )
    ordering = ('-start_time',)
