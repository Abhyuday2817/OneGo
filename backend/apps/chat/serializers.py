from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    read_by = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "room", "sender", "content", "timestamp",
            "read_by",
        ]
        read_only_fields = ["id", "timestamp", "sender", "read_by"]

class ChatRoomSerializer(serializers.ModelSerializer):
    participants       = UserSerializer(many=True, read_only=True)
    participant_ids    = serializers.PrimaryKeyRelatedField(
                            queryset=User.objects.all(),
                            many=True,
                            write_only=True,
                            source="participants"
                         )
    last_message       = serializers.SerializerMethodField()
    unread_count       = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            "id", "name", "participants", "participant_ids",
            "created_at", "last_message", "unread_count",
        ]
        read_only_fields = ["id", "created_at", "last_message", "unread_count"]

    def get_last_message(self, room):
        msg = room.messages.order_by("-timestamp").first()
        return MessageSerializer(msg, context=self.context).data if msg else None

    def get_unread_count(self, room):
        user = self.context["request"].user
        return room.messages.exclude(read_by=user).count()