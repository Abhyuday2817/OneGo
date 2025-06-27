from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review

@receiver([post_save, post_delete], sender=Review)
def recalc_rating(sender, instance, **kwargs):
    """
    Whenever a review is added/removed, update the mentor's average rating.
    """
    Review.update_mentor_rating(instance.reviewee)
