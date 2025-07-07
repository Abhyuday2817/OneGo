from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user", 
        "message", 
        "type", 
        "priority", 
        "unread", 
        "is_archived", 
        "created_at", 
        "expires_at"
    )
    list_filter = (
        "unread", 
        "is_archived", 
        "type", 
        "priority", 
        "created_at", 
        "expires_at"
    )
    search_fields = (
        "user__username", 
        "message", 
        "link"
    )
    readonly_fields = (
        "created_at", 
        "expires_at"
    )
    actions = [
        "mark_as_read", 
        "mark_as_unread", 
        "archive_selected", 
        "delete_expired"
    ]
    ordering = ("-created_at",)

    def mark_as_read(self, request, queryset):
        updated = queryset.filter(unread=True).update(unread=False)
        self.message_user(request, f"{updated} notifications marked as read.")

    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        updated = queryset.filter(unread=False).update(unread=True)
        self.message_user(request, f"{updated} notifications marked as unread.")

    mark_as_unread.short_description = "Mark selected as unread"

    def archive_selected(self, request, queryset):
        updated = queryset.filter(is_archived=False).update(is_archived=True)
        self.message_user(request, f"{updated} notifications archived.")

    archive_selected.short_description = "Archive selected notifications"

    def delete_expired(self, request, queryset):
        from django.utils import timezone
        expired = queryset.filter(expires_at__lt=timezone.now())
        count = expired.count()
        expired.delete()
        self.message_user(request, f"{count} expired notifications deleted.")

    delete_expired.short_description = "Delete expired notifications"
