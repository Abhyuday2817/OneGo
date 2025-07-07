from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.categories.models import Category
from apps.mentors.models import MentorProfile


class GigRequest(models.Model):
    STATUS_OPEN = "Open"
    STATUS_CANCELLED = "Cancelled"
    STATUS_CLOSED = "Closed"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_CLOSED, "Closed"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gigs_from_gigs_app"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="gigs_from_gigs_app"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget_min = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    budget_max = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    bidding_deadline = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["student", "status"]),
            models.Index(fields=["bidding_deadline"]),
        ]

    def __str__(self):
        return f"Gig #{self.pk}: {self.title}"

    def clean(self):
        if self.budget_max < self.budget_min:
            raise ValidationError("budget_max must be ≥ budget_min")
        if self.bidding_deadline <= timezone.now():
            raise ValidationError("bidding_deadline must be in the future")

    def is_open(self):
        return (
            self.status == self.STATUS_OPEN
            and timezone.now() < self.bidding_deadline
        )

    def cancel(self):
        self.status = self.STATUS_CANCELLED
        self.save()

    def close(self):
        self.status = self.STATUS_CLOSED
        self.save()

    def active_bids(self):
        return self.bids_from_gigs_app.filter(status=Bid.STATUS_PENDING)

    def accepted_bid(self):
        return self.bids_from_gigs_app.filter(status=Bid.STATUS_ACCEPTED).first()


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
        related_name="bids_from_gigs_app"
    )
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        related_name="bids_from_gigs_app"
    )
    proposed_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    proposal_text = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["gig_request", "mentor"]]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["mentor", "status"]),
            models.Index(fields=["gig_request", "status"]),
        ]

    def __str__(self):
        return f"Bid #{self.pk} by {self.mentor.user.username}"

    def accept(self):
        from apps.gigs.models import Contract
        self.gig_request.bids_from_gigs_app.exclude(pk=self.pk).update(status=self.STATUS_REJECTED)
        self.status = self.STATUS_ACCEPTED
        self.save()
        Contract.objects.create_from_bid(self)

    def reject(self):
        self.status = self.STATUS_REJECTED
        self.save()

    def is_winner(self):
        return self.status == self.STATUS_ACCEPTED

    def is_pending(self):
        return self.status == self.STATUS_PENDING


class Contract(models.Model):
    STATUS_ACTIVE = "Active"
    STATUS_COMPLETED = "Completed"
    STATUS_CANCELLED = "Cancelled"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    bid = models.OneToOneField(
        Bid, 
        on_delete=models.CASCADE, 
        related_name="contract_from_gigs_app"
    )
    gig_request = models.ForeignKey(
        GigRequest,
        on_delete=models.CASCADE,
        related_name="contracts_from_gigs_app"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contracts_as_student_from_gigs_app"
    )
    mentor = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        related_name="contracts_as_mentor_from_gigs_app"
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"Contract #{self.pk} ({self.bid})"

    @classmethod
    def create_from_bid(cls, bid):
        return cls.objects.create(
            bid=bid,
            gig_request=bid.gig_request,
            student=bid.gig_request.student,
            mentor=bid.mentor
        )

    def complete(self):
        self.status = self.STATUS_COMPLETED
        self.end_date = timezone.now()
        self.save()

    def cancel(self):
        self.status = self.STATUS_CANCELLED
        self.end_date = timezone.now()
        self.save()

    def is_active(self):
        return self.status == self.STATUS_ACTIVE

    def is_completed(self):
        return self.status == self.STATUS_COMPLETED

    def is_cancelled(self):
        return self.status == self.STATUS_CANCELLED
