# onego/backend/utils/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from reviews.models import Review
from sessions.models import Session
from badges.services import award_badge

@receiver(post_save, sender=Review)
def update_mentor_rating(sender, instance, **kwargs):
    """
    Recalculate the average rating of a mentor whenever a new Review is saved.
    """
    mentor = instance.reviewee
    agg = mentor.received_reviews.aggregate(avg=models.Avg("rating"), count=models.Count("id"))
    mentor.rating = agg["avg"] or 0
    mentor.num_reviews = agg["count"]
    mentor.save()

@receiver(post_save, sender=Session)
def session_completed_handler(sender, instance, **kwargs):
    """
    When a session flips to COMPLETED and both sides confirmed, verify & payout.
    """
    if instance.status == Session.STATUS_COMPLETED and instance.verified is False:
        instance.try_verify()
        # automatically release escrow
        from services.escrow import release_to_mentor
        release_to_mentor(instance)

@receiver(post_save, sender=Session)
def check_badge_milestones(sender, instance, created, **kwargs):
    """
    Award badges such as ‘first session completed’.
    """
    if created:
        return
    if instance.status == Session.STATUS_COMPLETED and instance.verified:
        award_badge(instance.mentor.user, "first-session")
