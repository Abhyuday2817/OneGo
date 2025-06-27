from django.contrib import admin
from .models import MentorReview


@admin.register(MentorReview)
class MentorReviewAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'student', 'rating', 'created_at')
    list_filter = ('mentor', 'student', 'rating', 'created_at')
    search_fields = ('mentor__user__username', 'student__username', 'review')