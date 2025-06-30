# onego/backend/badges/services.py

from django.utils import timezone
from .models import Badge, UserBadge

def award_badge(user, badge_code):
    """
    Give the user a badge (if they don't already have it).
    """
    try:
        badge = Badge.objects.get(code=badge_code)
    except Badge.DoesNotExist:
        return  # or log missing badge
    UserBadge.objects.get_or_create(user=user, badge=badge)
