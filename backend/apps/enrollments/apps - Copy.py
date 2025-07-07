from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.bids.models import Bid
from apps.notifications.models import Notification


@receiver(post_save, sender=Bid)
def notify_on_new_bid(sender, instance, created, **kwargs):
    """
    Sends a notification to the student when a mentor places a new bid.
    """
    if created:
        gig_request = instance.gig_request
        student = gig_request.student
        mentor = instance.mentor

        Notification.objects.create(
            user=student.user,
            message=f"{mentor.user.username} placed a bid on your learning request '{gig_request.title}'.",
            type="bid",
            link=f"/gigs/{gig_request.id}/bids/"
        )


@receiver(post_save, sender=Bid)
def notify_on_bid_acceptance(sender, instance, created, **kwargs):
    """
    Sends a notification to the mentor when their bid is accepted.
    This assumes the `status` field updates to 'accepted'.
    """
    if not created and instance.status == 'accepted':
        Notification.objects.create(
            user=instance.mentor.user,
            message=f"Your bid on '{instance.gig_request.title}' was accepted!",
            type="bid_accepted",
            link=f"/contracts/{instance.gig_request.id}/"
        )
