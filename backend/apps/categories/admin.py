from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'course_count')
    list_filter  = ('type',)
    search_fields= ('name',)
    
    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'Number of Courses'
