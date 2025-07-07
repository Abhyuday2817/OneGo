from django.contrib import admin
from .models import MentorProfile, AvailabilityWindow, MentorAvailability

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hourly_rate', 'per_minute_rate', 'rating', 'num_reviews', 'is_active', 'is_verified')
    list_filter  = ('rating', 'specialties', 'is_active', 'is_verified')
    search_fields = ('user__username', 'bio', 'certifications', 'languages', 'country', 'expertise')
    filter_horizontal = ('specialties',)

@admin.register(AvailabilityWindow)
class AvailabilityWindowAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'start', 'end', 'is_booked', 'created_at')
    list_filter = ('mentor', 'is_booked')
    search_fields = ('mentor__user__username',)

@admin.register(MentorAvailability)
class MentorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'day', 'start_time', 'end_time', 'is_available', 'timezone')
    list_filter = ('mentor', 'day', 'is_available')
    search_fields = ('mentor__user__username',)