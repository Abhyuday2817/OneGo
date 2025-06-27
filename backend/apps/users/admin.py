from django.contrib import admin
from .models import User
from apps.mentors.models import MentorProfile  # if needed
# from apps.students.models import StudentProfile  # if it exists

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "email")
