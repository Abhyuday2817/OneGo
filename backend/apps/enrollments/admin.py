# apps/enrollments/admin.py

from django.contrib import admin
from apps.enrollments.models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "completed", "enrolled_at")
    list_filter = ("completed", "enrolled_at")
    search_fields = ("student__username", "course__title")
    readonly_fields = ("progress", "enrolled_at")
