from django.contrib import admin
from .models import Session
from django.http import HttpResponse
from icalendar import Calendar
import csv


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "student", "mentor", "start_time",
        "end_time", "session_type", "status", "verified"
    )
    list_filter = ("status", "session_type", "verified")
    search_fields = ("student__username", "mentor__user__username")
    date_hierarchy = "start_time"
    actions = ["export_as_ics", "export_as_csv", "mark_completed"]

    def export_as_ics(self, request, queryset):
        cal = Calendar()
        cal.add("prodid", "-//OneGo Admin Export//onego.com//")
        cal.add("version", "2.0")
        for s in queryset:
            cal.add_component(s.to_ical_event())
        resp = HttpResponse(cal.to_ical(), content_type="text/calendar")
        resp["Content-Disposition"] = "attachment; filename=selected_sessions.ics"
        return resp
    export_as_ics.short_description = "Export selected sessions to iCal"

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=sessions_export.csv'

        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Student', 'Mentor', 'Start Time', 'End Time',
            'Session Type', 'Status', 'Verified', 'Duration (min)', 'Total Price'
        ])
        for s in queryset:
            writer.writerow([
                s.id, s.student.username, s.mentor.user.username,
                s.start_time, s.end_time, s.session_type,
                s.status, s.verified, s.duration_minutes, s.total_price
            ])
        return response
    export_as_csv.short_description = "Export selected sessions as CSV"

    def mark_completed(self, request, queryset):
        updated = queryset.update(status=Session.STATUS_COMPLETED)
        self.message_user(request, f"{updated} session(s) marked as completed.")
    mark_completed.short_description = "Mark selected sessions as completed"
