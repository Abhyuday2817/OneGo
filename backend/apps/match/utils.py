# apps/match/utils.py

from apps.mentors.models import MentorProfile
from apps.users.models import User
from django.db.models import Q

def smart_match_mentors(category=None, language=None, budget=None, country=None, min_rating=4):
    """
    Returns a list of mentor profiles matching student preferences.
    Filters by skill category, language, budget, rating, and location.
    """

    mentors = MentorProfile.objects.filter(
        Q(skills__icontains=category) if category else Q(),
        Q(languages__icontains=language) if language else Q(),
        Q(country__iexact=country) if country else Q(),
        Q(rate_per_minute__lte=budget) if budget else Q(),
        Q(user__ratings__average__gte=min_rating) if min_rating else Q(),
        user__is_active=True,
        user__is_mentor=True,
        is_verified=True
    ).distinct()

    return mentors

def rank_mentors(mentors):
    """
    Optionally rank mentors by rating, response time, or number of courses
    """
    return sorted(mentors, key=lambda m: (m.average_rating or 0, -m.total_sessions()), reverse=True)
