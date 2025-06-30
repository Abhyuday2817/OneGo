# apps/bids/models.py

from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from apps.gigs.models import GigRequest
from apps.mentors.models import MentorProfile
from services.notifications import notify_user  # custom notification handler


class Bid(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_ACCEPTED = "Accepted"
    STATUS_REJECTED = "Rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
    ]

    gig_request = models.ForeignKey(
        GigRequest,
        on_delete=models.CASCADE,
        related_name="bids_from_bids_app"
    )
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        related_name="bids_from_bids_app"
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
        return f"Bid #{self.pk} by {self.mentor.user.username} on Gig #{self.gig_request.pk}"

    def clean(self):
        """Ensure bidding rules are respected."""
        if not self.gig_request.is_open():
            raise ValidationError("Cannot bid on a closed or expired gig.")

    def accept(self):
        """
        Accept this bid:
        - Reject all others
        - Notify student and mentor
        """
        with transaction.atomic():
            self.gig_request.bids_from_bids_app.exclude(pk=self.pk).update(status=self.STATUS_REJECTED)
            self.status = self.STATUS_ACCEPTED
            self.save()
            notify_user(
                self.gig_request.student,
                f"Your gig request “{self.gig_request.title}” accepted a bid by {self.mentor.user.username}."
            )
            notify_user(
                self.mentor.user,
                f"You have been awarded the gig “{self.gig_request.title}”. Congratulations!"
            )

    def reject(self):
        self.status = self.STATUS_REJECTED
        self.save()
        notify_user(
            self.mentor.user,
            f"Your bid on gig “{self.gig_request.title}” was not selected."
        )

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_accepted(self):
        return self.status == self.STATUS_ACCEPTED

    def is_rejected(self):
        return self.status == self.STATUS_REJECTED
