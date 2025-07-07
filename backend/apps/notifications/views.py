from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Handles notifications:
    - List, retrieve
    - Mark as read (single & all)
    - Count unread
    - Archive, prioritize
    - Delete individual & bulk
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message", "type"]
    ordering_fields = ["created_at", "expires_at", "priority"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)

        # Optional filters
        type_filter = self.request.query_params.get("type")
        priority_filter = self.request.query_params.get("priority")
        is_archived = self.request.query_params.get("archived")

        if type_filter:
            queryset = queryset.filter(type=type_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        if is_archived is not None:
            if is_archived.lower() == "true":
                queryset = queryset.filter(is_archived=True)
            elif is_archived.lower() == "false":
                queryset = queryset.filter(is_archived=False)

        return queryset.order_by("-created_at")

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        """
        POST /notifications/{id}/mark-read/
        """
        notification = self.get_object()
        notification.unread = False
        notification.save()
        return Response({"status": "Notification marked as read."})

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        """
        POST /notifications/mark-all-read/
        """
        count = Notification.objects.filter(user=request.user, unread=True).update(unread=False)
        return Response({"marked": count, "status": "All notifications marked as read."})

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        """
        GET /notifications/unread-count/
        """
        count = Notification.objects.filter(user=request.user, unread=True).count()
        return Response({"unread_count": count})

    @action(detail=True, methods=["post"], url_path="archive")
    def archive(self, request, pk=None):
        """
        POST /notifications/{id}/archive/
        """
        notification = self.get_object()
        notification.is_archived = True
        notification.save()
        return Response({"status": "Notification archived."})

    @action(detail=True, methods=["post"], url_path="mark-important")
    def mark_important(self, request, pk=None):
        """
        POST /notifications/{id}/mark-important/
        """
        notification = self.get_object()
        notification.priority = "high"
        notification.save()
        return Response({"status": "Notification marked as important."})

    @action(detail=False, methods=["delete"], url_path="bulk-delete")
    def bulk_delete(self, request):
        """
        DELETE /notifications/bulk-delete/
        Optional query: ?archived=true to delete archived only
        """
        qs = Notification.objects.filter(user=request.user)
        if request.query_params.get("archived") == "true":
            qs = qs.filter(is_archived=True)
        count = qs.delete()[0]
        return Response({"deleted": count})
