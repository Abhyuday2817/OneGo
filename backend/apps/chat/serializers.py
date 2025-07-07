from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message, Attachment, Reaction, ChatMembership

User = get_user_model()


# 🔹 User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


# 🔹 Attachment Serializer
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id", "file", "uploaded_at"]


# 🔹 Reaction Serializer
class ReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = ["id", "emoji", "user", "reacted_at"]
        read_only_fields = ["id", "user", "reacted_at"]


# 🔹 Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    read_by = UserSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    reactions = ReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "room", "sender", "receiver", "content",
            "sent_at", "read_by", "edited_at", "deleted",
            "pinned", "system_message", "attachments", "reactions"
        ]
        read_only_fields = [
            "id", "sender", "sent_at", "read_by", "edited_at",
            "deleted", "pinned", "system_message", "attachments", "reactions"
        ]


# 🔹 ChatRoom Serializer
class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source="members"
    )
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            "id", "name", "is_group", "members", "member_ids",
            "created_at", "last_message", "unread_count"
        ]
        read_only_fields = ["id", "created_at", "last_message", "unread_count", "members"]

    def get_last_message(self, room):
        last_msg = room.messages.order_by("-sent_at").first()
        return MessageSerializer(last_msg, context=self.context).data if last_msg else None

    def get_unread_count(self, room):
        user = self.context["request"].user
        return room.messages.exclude(read_by=user).count()

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        room = ChatRoom.objects.create(**validated_data)
        room.members.set(members + [self.context["request"].user])
        return room


# 🔹 ChatMembership Serializer (Optional: Admin View or Moderation Panel)
class ChatMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ChatMembership
        fields = ["id", "user", "room", "joined_at", "nickname", "muted_until"]
