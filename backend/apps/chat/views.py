from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer, UserSerializer

User = get_user_model()

class ChatRoomViewSet(viewsets.ModelViewSet):
    """
    list/retrieve/create/update/delete chat rooms with actions:
    - add/remove participant
    - rename room
    - analytics on message counts
    """
    queryset = ChatRoom.objects.prefetch_related("participants", "messages").all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "participants__username"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        room = serializer.save()
        room.participants.add(self.request.user)

    @action(detail=True, methods=["post"], url_path="add")
    def add_participant(self, request, pk=None):
        room = self.get_object()
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
            room.participants.add(user)
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
            room.participants.remove(user)
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


class MessageViewSet(viewsets.ModelViewSet):
    """
    list/retrieve/create/update/delete messages with:
    - mark-read, edit, delete message
    """
    queryset = Message.objects.select_related("sender", "room").prefetch_related("read_by").all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["content", "sender__username"]
    ordering_fields = ["timestamp"]
    ordering = ["timestamp"]

    def get_queryset(self):
        qs = self.queryset.filter(room__participants=self.request.user)
        room_id = self.request.query_params.get("room")
        if room_id:
            qs = qs.filter(room_id=room_id)
        before = self.request.query_params.get("before")
        after  = self.request.query_params.get("after")
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
        msg.save()
        return Response(MessageSerializer(msg, context=self.get_serializer_context()).data)

    @action(detail=True, methods=["delete"], url_path="delete")
    def delete_message(self, request, pk=None):
        msg = self.get_object()
        if msg.sender != request.user:
            return Response({"error": "cannot delete others' messages"}, status=status.HTTP_403_FORBIDDEN)
        msg.delete()
        return Response({"status": "deleted"}, status=status.HTTP_204_NO_CONTENT)


from rest_framework import generics

class UserSearchView(generics.ListAPIView):
    """
    GET /api/chat/users/?q=<username_substring>
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "first_name", "last_name"]

    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)
