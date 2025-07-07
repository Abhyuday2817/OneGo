from django.contrib import admin
from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "topic",
        "mentor_name",
        "student_name",
        "scheduled_time",
        "duration_mins",
        "status",
        "twilio_room_sid",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "scheduled_time",
        "mentor",
        "student",
    )
    search_fields = (
        "topic",
        "mentor__user__username",
        "student__username",
        "mentor__user__email",
        "student__email",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "twilio_room_sid",
        "end_time",
        "feedback",
        "rating",
    )
    ordering = ("-scheduled_time",)
    date_hierarchy = "scheduled_time"

    def mentor_name(self, obj):
        return obj.mentor.user.username
    mentor_name.short_description = "Mentor"

    def student_name(self, obj):
        return obj.student.username
    student_name.short_description = "Student"

    def has_add_permission(self, request):
        """Prevent manual admin creation"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion unless superuser"""
        return request.user.is_superuser
