from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Handles listing, retrieving, marking as read, and bulk operations on notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-timestamp")

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        """
        Mark a single notification as read.
        """
        notification = self.get_object()
        notification.unread = False
        notification.save()
        return Response({"status": "Notification marked as read."})

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        """
        Mark all unread notifications as read for the current user.
        """
        count = Notification.objects.filter(user=request.user, unread=True).update(unread=False)
        return Response({"marked": count, "status": "All notifications marked as read."})

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        """
        Get count of unread notifications for the current user.
        """
        count = Notification.objects.filter(user=request.user, unread=True).count()
        return Response({"unread_count": count})
