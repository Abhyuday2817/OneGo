from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ("Programming", "Programming"),
    ("Design", "Design"),
    ("Marketing", "Marketing"),
    ("Music", "Music"),
    ("Language", "Language"),
    ("Other", "Other"),
]

class LearningRequest(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_requests")
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_language = models.CharField(max_length=50, blank=True, null=True)
    timeline_days = models.PositiveIntegerField(help_text="Preferred completion time in days")
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.student.username}"

class LearningRequestProposal(models.Model):
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="proposals")
    request = models.ForeignKey(LearningRequest, on_delete=models.CASCADE, related_name="proposals")
    proposal_text = models.TextField()
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField()
    is_selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mentor', 'request')

    def __str__(self):
        return f"Proposal by {self.mentor.username} for {self.request.title}"
