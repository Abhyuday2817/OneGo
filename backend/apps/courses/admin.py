from django.contrib import admin
from .models import Course, CourseQuiz
from apps.enrollments.models import Enrollment  # Import Enrollment model


class CourseQuizInline(admin.TabularInline):
    model = CourseQuiz
    extra = 1


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ("student", "enrolled_at")
    fields = ("student", "enrolled_at")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "mentor", "category", "delivery_type", "price", "created_at")
    list_filter  = ("delivery_type", "category", "created_at")
    search_fields = ("title", "description", "mentor__user__username")
    readonly_fields = ("created_at", "updated_at")
    inlines = [CourseQuizInline, EnrollmentInline]


@admin.register(CourseQuiz)
class CourseQuizAdmin(admin.ModelAdmin):
    list_display = ("course", "question", "correct_answer")
    search_fields = ("course__title", "question")
