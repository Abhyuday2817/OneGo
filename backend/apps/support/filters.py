# apps/support/filters.py

import django_filters
from .models import SupportTicket

class SupportTicketFilter(django_filters.FilterSet):
    class Meta:
        model = SupportTicket
        fields = ['status', 'priority', 'assigned_to']
