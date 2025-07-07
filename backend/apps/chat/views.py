from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer, UserSerializer

User = get_user_model()


# 🔹 ChatRoom ViewSet
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.prefetch_related("members", "messages").all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "members__username"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ChatRoom.objects.none()
        return self.queryset.filter(members=self.request.user)

    def perform_create(self, serializer):
        room = serializer.save()
        room.members.add(self.request.user)

    @action(detail=True, methods=["post"], url_path="add")
    def add_participant(self, request, pk=None):
        room = self.get_object()
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
            room.members.add(user)
            return Response({"status": f"added {user.username}"})
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"], url_path="remove")
    def remove_participant(self, request, pk=None):
        room = self.get_object()
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
            room.members.remove(user)
            return Response({"status": f"removed {user.username}"})
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"], url_path="rename")
    def rename_room(self, request, pk=None):
        room = self.get_object()
        name = request.data.get("name", "").strip()
        if not name:
            return Response({"error": "name cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        room.name = name
        room.save()
        return Response({"status": f"renamed to {name}"})

    @action(detail=True, methods=["post"], url_path="mute")
    def mute_room(self, request, pk=None):
        # Optional: track muted rooms if you have a mute model
        return Response({"status": "muted notifications for this room"})

    @action(detail=True, methods=["get"], url_path="analytics")
    def analytics(self, request, pk=None):
        room = self.get_object()
        total = room.messages.count()
        unread = room.messages.exclude(read_by=request.user).count()
        by_user = (
            room.messages.values("sender__username")
                         .annotate(count=Count("id"))
                         .order_by("-count")
        )
        return Response({
            "total_messages": total,
            "unread_messages": unread,
            "active_users": by_user,
        })


# 🔹 Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related("sender", "room").prefetch_related("read_by").all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["content", "sender__username"]
    ordering_fields = ["timestamp"]
    ordering = ["timestamp"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Message.objects.none()

        qs = self.queryset.filter(room__members=self.request.user)
        room_id = self.request.query_params.get("room")
        if room_id:
            qs = qs.filter(room_id=room_id)

        before = self.request.query_params.get("before")
        after = self.request.query_params.get("after")

        if before:
            qs = qs.filter(timestamp__lte=before)
        if after:
            qs = qs.filter(timestamp__gte=after)

        return qs

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        msg = self.get_object()
        msg.read_by.add(request.user)
        return Response({"status": "marked as read"})

    @action(detail=True, methods=["post"], url_path="edit")
    def edit(self, request, pk=None):
        msg = self.get_object()
        if msg.sender != request.user:
            return Response({"error": "cannot edit others' messages"}, status=status.HTTP_403_FORBIDDEN)
        text = request.data.get("content", "").strip()
        if not text:
            return Response({"error": "content cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        msg.content = text
        msg.edited_at = timezone.now()
        msg.save()
        return Response(MessageSerializer(msg, context=self.get_serializer_context()).data)

    @action(detail=True, methods=["delete"], url_path="delete")
    def delete_message(self, request, pk=None):
        msg = self.get_object()
        if msg.sender != request.user:
            return Response({"error": "cannot delete others' messages"}, status=status.HTTP_403_FORBIDDEN)
        msg.delete()
        return Response({"status": "deleted"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_path="react")
    def react(self, request, pk=None):
        emoji = request.data.get("emoji", "👍")
        # You can implement a Reaction model later
        return Response({"status": f"reacted with {emoji}"})


# 🔍 User Search
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name"]

    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)
