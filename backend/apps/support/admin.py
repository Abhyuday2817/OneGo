# support/admin.py
from django.contrib import admin
from .models import SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'user', 'status', 'priority', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('subject', 'message', 'user__username')
    ordering = ('-created_at',)
