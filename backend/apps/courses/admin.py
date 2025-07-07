from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg

from .models import Course
from apps.enrollments.models import Enrollment


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ("student", "enrolled_at", "progress")  # Removed "status"
    fields = ("student", "enrolled_at", "progress")           # Removed "status"
    show_change_link = False


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "mentor_username",
        "category",
        "delivery_type",
        "price",
        "is_published",
        "enrollments_count",
        "average_rating",
        "created_at",
        "preview_link",
    )
    list_filter = (
        "delivery_type",
        "category",
        "published",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "mentor__user__username",
        "category__name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "enrollments_count",
        "average_rating",
    )
    inlines = [EnrollmentInline]
    actions = [
        "mark_as_published",
        "mark_as_unpublished",
    ]

    def mentor_username(self, obj):
        return obj.mentor.user.username
    mentor_username.short_description = "Mentor"

    def preview_link(self, obj):
        if obj.preview_video:
            return format_html(f"<a href='{obj.preview_video}' target='_blank'>Preview</a>")
        return "-"
    preview_link.short_description = "Preview Video"

    def is_published(self, obj):
        return format_html("<b style='color:green;'>Yes</b>") if getattr(obj, "published", False) else "No"
    is_published.short_description = "Published"

    def enrollments_count(self, obj):
        return obj.enrollment_set.count()
    enrollments_count.short_description = "Enrolled Students"

    def average_rating(self, obj):
        return round(
            obj.enrollment_set.aggregate(avg=Avg("rating"))["avg"] or 0, 2
        )
    average_rating.short_description = "Avg Rating"

    @admin.action(description="Mark selected courses as Published")
    def mark_as_published(self, request, queryset):
        queryset.update(published=True)

    @admin.action(description="Mark selected courses as Unpublished")
    def mark_as_unpublished(self, request, queryset):
        queryset.update(published=False)
