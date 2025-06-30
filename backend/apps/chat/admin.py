from django.contrib import admin
from .models import Message, ChatRoom

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("room", "sender", "receiver", "sent_at", "content")
    search_fields = ("sender__username", "receiver__username", "content")
    list_filter = ("sent_at", "room")

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)