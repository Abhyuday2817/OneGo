from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import SupportTicket
from .serializers import (
    SupportTicketSerializer,
    SupportTicketCreateSerializer,
    SupportTicketUpdateSerializer,
    SupportTicketStatusSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()


class SupportTicketViewSet(viewsets.ModelViewSet):
    """
    Handles all CRUD operations for support tickets.
    - Authenticated users can create, list, view their tickets
    - Admins can assign, close, reopen, and analyze tickets
    """
    queryset = SupportTicket.objects.select_related("user", "assigned_to").all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "priority", "status"]
    ordering = ["-created_at"]
    search_fields = ["subject", "message", "resolution"]

    def get_queryset(self):
        user = self.request.user
        return self.queryset if user.is_staff else self.queryset.filter(user=user)

    def get_serializer_class(self):
        if self.action == "create":
            return SupportTicketCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return SupportTicketUpdateSerializer
        elif self.action in ["close", "reopen", "mark_in_progress"]:
            return SupportTicketStatusSerializer
        return SupportTicketSerializer

    def create(self, request, *args, **kwargs):
        """
        Overrides default create to return full ticket data after creation.
        """
        create_serializer = SupportTicketCreateSerializer(data=request.data, context={'request': request})
        create_serializer.is_valid(raise_exception=True)
        ticket = create_serializer.save(user=request.user)

        read_serializer = SupportTicketSerializer(ticket, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        """
        POST /api/support/{id}/assign/
        Assign a ticket to a staff member.
        """
        if not request.user.is_staff:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        ticket = self.get_object()
        assignee_id = request.data.get("assigned_to")
        if not assignee_id:
            return Response({"error": "assigned_to is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            assignee = User.objects.get(pk=assignee_id, is_staff=True)
            ticket.assign_to(assignee)
            return Response({"status": f"Assigned to {assignee.username}"})
        except User.DoesNotExist:
            return Response({"error": "User not found or not staff."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        """
        POST /api/support/{id}/close/
        Close a ticket with an optional resolution message.
        """
        ticket = self.get_object()
        if ticket.status == SupportTicket.STATUS_CLOSED:
            return Response({"detail": "Ticket is already closed."})

        resolution = request.data.get("resolution", "")
        ticket.close_ticket(resolution)
        return Response({"status": "closed", "closed_at": ticket.closed_at})

    @action(detail=True, methods=["post"])
    def reopen(self, request, pk=None):
        """
        POST /api/support/{id}/reopen/
        Reopen a closed ticket.
        """
        ticket = self.get_object()
        if ticket.status != SupportTicket.STATUS_CLOSED:
            return Response({"detail": "Ticket is not closed."}, status=400)

        ticket.reopen_ticket()
        return Response({"status": "reopened"})

    @action(detail=True, methods=["post"])
    def mark_in_progress(self, request, pk=None):
        """
        POST /api/support/{id}/mark_in_progress/
        Mark a ticket as in progress.
        """
        ticket = self.get_object()
        if ticket.status == SupportTicket.STATUS_IN_PROGRESS:
            return Response({"detail": "Ticket is already in progress."})

        ticket.mark_in_progress()
        return Response({"status": "in_progress"})

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        GET /api/support/stats/
        Returns counts grouped by status and priority.
        """
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = {
            "status_counts": SupportTicket.objects.values("status").annotate(count=Count("id")),
            "priority_counts": SupportTicket.objects.values("priority").annotate(count=Count("id")),
        }
        return Response(data)
