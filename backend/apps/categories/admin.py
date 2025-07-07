from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'course_count', 'has_free_courses', 'average_price')
    list_filter  = ('type',)
    search_fields = ('name', 'description')
    ordering = ('type', 'name')

    def course_count(self, obj):
        return obj.total_courses()
    course_count.short_description = 'Courses'

    def has_free_courses(self, obj):
        try:
            return obj.has_free_courses()
        except Exception:
            return False
    has_free_courses.boolean = True
    has_free_courses.short_description = 'Free?'

    def average_price(self, obj):
        try:
            return f"₹{obj.average_price():.2f}"
        except Exception:
            return "-"
    average_price.short_description = 'Avg Price'
