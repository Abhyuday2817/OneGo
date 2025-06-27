# courses/admin.py
from django.contrib import admin
from .models import Course
from apps.enrollments.models import Enrollment  # ✅ CORRECT

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ("student", "enrolled_at")
    fields = ("student", "enrolled_at")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "mentor", "category", "delivery_type", "price", "created_at")
    list_filter  = ("delivery_type", "category")
    search_fields = ("title", "description", "mentor__user__username")
    inlines = [EnrollmentInline]
    readonly_fields = ("created_at", "updated_at")
