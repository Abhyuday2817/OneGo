# onego/backend/services/calendar.py

from icalendar import Calendar, Event
from django.utils.timezone import localtime

def generate_ical_for_user(user):
    """
    Build an iCal feed of all upcoming verified sessions for this user.
    """
    from sessions.models import Session

    cal = Calendar()
    cal.add("prodid", "-//OneGo Learning Marketplace//onego.com//")
    cal.add("version", "2.0")

    upcoming = Session.objects.filter(
        (models.Q(student=user) | models.Q(mentor__user=user)),
        start_time__gte=localtime()
    )

    for session in upcoming:
        ev = Event()
        ev.add("uid", f"session-{session.pk}@onego.com")
        ev.add("dtstart", localtime(session.start_time))
        ev.add("dtend",   localtime(session.end_time))
        ev.add("summary", f"{session.session_type} session with "
                          f"{session.mentor.user.username if session.student == user else session.student.username}")
        ev.add("description", f"Type: {session.session_type}\n"
                              f"Rate: {session.rate_applied}")
        cal.add_component(ev)

    return cal.to_ical()
