from django.utils import timezone
from django.db import IntegrityError
from .models import Badge, UserBadge
from sessions.models import Session
from reviews.models import Review

def award_badge(user, badge_slug):
    """
    Award the badge identified by badge_slug to user, if not already.
    Returns True if newly awarded, False if already had it or slug invalid.
    """
    try:
        badge = Badge.objects.get(slug=badge_slug)
    except Badge.DoesNotExist:
        return False

    try:
        UserBadge.objects.create(user=user, badge=badge)
        return True
    except IntegrityError:
        # already awarded
        return False


def check_first_session(user):
    """
    If user has completed and verified at least one session, award 'first-session'.
    """
    count = Session.objects.filter(
        student=user, status=Session.STATUS_COMPLETED, verified=True
    ).count()
    if count >= 1:
        return award_badge(user, "first-session")
    return False


def check_five_star_mentor(user):
    """
    Award 'five-star-mentor' if user is a mentor with avg rating >= 5 and >= 10 reviews.
    """
    from mentors.models import MentorProfile
    try:
        mp = MentorProfile.objects.get(user=user)
    except MentorProfile.DoesNotExist:
        return False

    if mp.rating >= 5.0 and mp.num_reviews >= 10:
        return award_badge(user, "five-star-mentor")
    return False


def check_session_count(user, threshold, slug):
    """
    Award badge 'slug' if user has delivered >= threshold sessions as mentor.
    """
    from sessions.models import Session
    count = Session.objects.filter(
        mentor__user=user, status=Session.STATUS_COMPLETED, verified=True
    ).count()
    if count >= threshold:
        return award_badge(user, slug)
    return False


def run_all_milestone_checks(user):
    """
    Convenience to run all automatic badge checks for this user.
    """
    changed = []
    if check_first_session(user):
        changed.append("first-session")
    if check_five_star_mentor(user):
        changed.append("five-star-mentor")
    # e.g. badges for 10, 50, 100 sessions
    for thresh, slug in [(10, "mentor-10-sessions"), (50, "mentor-50-sessions")]:
        if check_session_count(user, thresh, slug):
            changed.append(slug)
    return changed
