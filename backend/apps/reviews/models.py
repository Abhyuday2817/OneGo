# apps/reviews/models.py

from django.db import models
from django.conf import settings
from apps.mentors.models import MentorProfile  # ✅ Correct import

class ReviewQuerySet(models.QuerySet):
    def for_mentor(self, mentor_profile):
        return self.filter(reviewee=mentor_profile)

class Review(models.Model):
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )
    reviewee = models.ForeignKey(
        MentorProfile,
        on_delete=models.CASCADE,
        related_name="received_reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ReviewQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["reviewer", "reviewee", "created_at"]]
        indexes = [
            models.Index(fields=["reviewee", "created_at"]),
            models.Index(fields=["reviewer", "created_at"]),
        ]

    def __str__(self):
        return f"Review by {self.reviewer.username} → {self.reviewee.user.username} ({self.rating}/5)"

    @classmethod
    def update_mentor_rating(cls, mentor_profile):
        agg = cls.objects.for_mentor(mentor_profile).aggregate(avg=models.Avg("rating"))
        mentor_profile.rating = agg["avg"] or 0
        mentor_profile.save()
