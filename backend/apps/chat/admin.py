from django.contrib import admin
from .models import ChatRoom, ChatMembership, Message, Attachment


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_group", "created_at", "member_count")
    search_fields = ("name",)
    list_filter = ("is_group",)
    readonly_fields = ("created_at",)

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = "Members"


@admin.register(ChatMembership)
class ChatMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "nickname", "muted_until", "joined_at")
    search_fields = ("user__username", "room__name", "nickname")
    list_filter = ("muted_until",)
    autocomplete_fields = ("user", "room")


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    readonly_fields = ("uploaded_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "sender", "receiver", "short_content", "sent_at", "edited_at", "deleted")
    search_fields = ("sender__username", "receiver__username", "content")
    list_filter = ("sent_at", "deleted", "edited_at")
    autocomplete_fields = ("room", "sender", "receiver")
    readonly_fields = ("sent_at", "edited_at")
    inlines = [AttachmentInline]

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = "Message"


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "file", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    search_fields = ("message__content",)
