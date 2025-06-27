# onego/backend/services/availability.py

from django.db.models import Q

def is_available(mentor, start, end):
    """
    Check that `mentor` has no overlapping sessions in [start, end).
    """
    from sessions.models import Session

    conflicts = Session.objects.filter(
        mentor=mentor,
        status__in=[Session.STATUS_SCHEDULED, Session.STATUS_COMPLETED],
    ).filter(
        Q(start_time__lt=end, end_time__gt=start)
    )
    return not conflicts.exists()
