from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now
from apps.enrollments.models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "progress_percent_display",
        "modules_remaining",
        "completed",
        "enrolled_days_ago",
        "enrolled_at",
    )
    list_filter = ("completed", "enrolled_at", "course")
    search_fields = ("student__username", "course__title")
    readonly_fields = ("progress_json", "enrolled_at", "progress_percent_display", "modules_remaining")
    ordering = ("-enrolled_at",)
    actions = ["mark_as_completed", "reset_progress"]

    def progress_json(self, obj):
        """Formatted view of progress JSON."""
        if not obj.progress:
            return "No progress yet"
        html = "<ul style='margin:0;padding-left:16px;'>"
        for module, percent in obj.progress.items():
            html += f"<li><strong>{module}:</strong> {percent}%</li>"
        html += "</ul>"
        return format_html(html)

    progress_json.short_description = "Progress Details"
    progress_json.allow_tags = True

    def progress_percent_display(self, obj):
        return f"{obj.progress_percent}%"

    progress_percent_display.short_description = "Avg. Progress"

    def enrolled_days_ago(self, obj):
        return f"{obj.days_since_enrollment}d ago"

    enrolled_days_ago.short_description = "Enrolled"

    def mark_as_completed(self, request, queryset):
        for enrollment in queryset:
            enrollment.mark_complete()
        self.message_user(request, f"{queryset.count()} enrollment(s) marked as complete.")

    mark_as_completed.short_description = "Mark selected as completed"

    def reset_progress(self, request, queryset):
        for enrollment in queryset:
            enrollment.reset_progress()
        self.message_user(request, f"{queryset.count()} enrollment(s) progress reset to 0%.")

    reset_progress.short_description = "Reset progress to 0%"
