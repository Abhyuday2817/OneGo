from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.gigs.models import GigRequest
from apps.mentors.models import MentorProfile
from services.notifications import notify_user


class BidQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status=Bid.STATUS_PENDING)

    def accepted(self):
        return self.filter(status=Bid.STATUS_ACCEPTED)

    def rejected(self):
        return self.filter(status=Bid.STATUS_REJECTED)


class Bid(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_ACCEPTED = "Accepted"
    STATUS_REJECTED = "Rejected"
    STATUS_CANCELLED = "Cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    gig_request = models.ForeignKey(
        GigRequest,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    proposed_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Rate proposed by mentor for completing the gig"
    )
    proposal_text = models.TextField(help_text="Explain your approach or value offer")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BidQuerySet.as_manager()

    class Meta:
        unique_together = [["gig_request", "mentor"]]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["mentor", "status"]),
            models.Index(fields=["gig_request", "status"]),
        ]
        verbose_name = "Bid"
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"Bid #{self.pk} by {self.mentor.user.username} for Gig #{self.gig_request.pk}"

    def clean(self):
        if not self.gig_request.is_open():
            raise ValidationError("Cannot bid on a closed or expired gig.")
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError("Invalid status for bid.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def accept(self):
        """Accept this bid and reject all others."""
        with transaction.atomic():
            self.gig_request.bids.exclude(pk=self.pk).update(status=self.STATUS_REJECTED)
            self.status = self.STATUS_ACCEPTED
            self.save()
            self.notify_status_change("accepted")

    def reject(self):
        """Reject this bid."""
        self.status = self.STATUS_REJECTED
        self.save()
        self.notify_status_change("rejected")

    def cancel(self):
        """Mentor cancels their bid voluntarily."""
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_CANCELLED
            self.save()
            self.notify_status_change("cancelled")

    def notify_status_change(self, change_type):
        """Send notifications to mentor and student based on status update."""
        title = self.gig_request.title
        student = self.gig_request.student
        mentor_user = self.mentor.user

        if change_type == "accepted":
            notify_user(student, f"Your gig '{title}' accepted a bid from {mentor_user.username}.")
            notify_user(mentor_user, f"Congrats! Your bid on '{title}' was accepted.")
        elif change_type == "rejected":
            notify_user(mentor_user, f"Your bid on gig '{title}' was not selected.")
        elif change_type == "cancelled":
            notify_user(student, f"{mentor_user.username} has cancelled their bid on your gig '{title}'.")

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_accepted(self):
        return self.status == self.STATUS_ACCEPTED

    def is_rejected(self):
        return self.status == self.STATUS_REJECTED

    def is_cancelled(self):
        return self.status == self.STATUS_CANCELLED
