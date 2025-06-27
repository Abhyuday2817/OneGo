from django.contrib import admin
from .models import MentorProfile

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hourly_rate', 'per_minute_rate', 'rating', 'num_reviews')
    list_filter  = ('rating', 'specialties')
    search_fields = ('user__username', 'bio', 'certifications')
    filter_horizontal = ('specialties',)
