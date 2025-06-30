# apps/consultations/admin.py
from django.contrib import admin
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "topic", "mentor", "student", "scheduled_time",
        "duration_mins", "status", "twilio_room_sid"
    )
    list_filter = ("status", "scheduled_time", "mentor")
    search_fields = ("topic", "student__username", "mentor__user__username")
    readonly_fields = ("created_at", "updated_at", "twilio_room_sid")  # Removed 'recording_url'
