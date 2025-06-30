from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import SupportTicket
from .serializers import SupportTicketSerializer
from .filters import SupportTicketFilter  # Optional: if you want advanced filtering


class SupportTicketViewSet(viewsets.ModelViewSet):
    """
    Handles all CRUD operations for support tickets.
    - Authenticated users can list, create, and update their own tickets
    - Admins can access and manage all tickets
    """
    queryset = SupportTicket.objects.select_related("user", "assigned_to").all()
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "priority", "status"]
    ordering = ["-created_at"]
    search_fields = ["subject", "message", "resolution"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        """
        POST /api/support/{id}/assign/
        Admin assigns a ticket to themselves or another staff member.
        """
        if not request.user.is_staff:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        ticket = self.get_object()
        assignee_id = request.data.get("assigned_to")
        if not assignee_id:
            return Response({"error": "assigned_to is required."}, status=status.HTTP_400_BAD_REQUEST)

        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            assignee = User.objects.get(pk=assignee_id, is_staff=True)
            ticket.assigned_to = assignee
            ticket.save()
            return Response({"status": f"Assigned to {assignee.username}"})
        except User.DoesNotExist:
            return Response({"error": "User not found or not staff."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        GET /api/support/stats/
        Admin stats on ticket counts by status & priority.
        """
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = {
            "status_counts": SupportTicket.objects.values("status").annotate(count=Count("id")),
            "priority_counts": SupportTicket.objects.values("priority").annotate(count=Count("id")),
        }
        return Response(data)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        """
        POST /api/support/{id}/close/
        Marks the ticket as closed.
        """
        ticket = self.get_object()
        if ticket.status == "closed":
            return Response({"detail": "Ticket is already closed."})
        ticket.status = "closed"
        ticket.closed_at = timezone.now()
        ticket.save()
        return Response({"status": "closed"})
