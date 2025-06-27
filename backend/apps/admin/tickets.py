from django.apps import apps
from django.db.models import Count, Q
from django.utils import timezone

# Assumes you have a SupportTicket model in a 'support' app
Ticket = apps.get_model("support", "SupportTicket")

def list_open_tickets(priority=None, days_open=None):
    """
    Fetch open tickets, optionally filtered by priority or how long they've been open.
    """
    qs = Ticket.objects.filter(status="open")
    if priority:
        qs = qs.filter(priority=priority)
    if days_open:
        cutoff = timezone.now() - timezone.timedelta(days=days_open)
        qs = qs.filter(created_at__lte=cutoff)
    return qs.order_by("-created_at")

def assign_ticket(ticket_id, admin_user):
    """
    Assigns the ticket to the given admin user.
    """
    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.assigned_to = admin_user
    ticket.status = "in_progress"
    ticket.save(update_fields=["assigned_to", "status", "updated_at"])
    return ticket

def escalate_ticket(ticket_id):
    """
    Bumps ticket priority by one level (low→medium→high→urgent).
    """
    ticket = Ticket.objects.get(pk=ticket_id)
    levels = ["low", "medium", "high", "urgent"]
    try:
        idx = levels.index(ticket.priority)
        ticket.priority = levels[min(idx + 1, len(levels) - 1)]
        ticket.save(update_fields=["priority", "updated_at"])
    except ValueError:
        pass
    return ticket

def close_ticket(ticket_id, resolution_notes=""):
    """
    Marks a ticket closed, records resolution notes.
    """
    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.status = "closed"
    ticket.resolution = resolution_notes
    ticket.closed_at = timezone.now()
    ticket.save(update_fields=["status", "resolution", "closed_at", "updated_at"])
    return ticket

def ticket_statistics():
    """
    Returns counts of tickets by status and priority.
    """
    by_status = Ticket.objects.values("status").annotate(count=Count("id"))
    by_priority = Ticket.objects.values("priority").annotate(count=Count("id"))
    return {
        "status_counts": {item["status"]: item["count"] for item in by_status},
        "priority_counts": {item["priority"]: item["count"] for item in by_priority},
    }
