### 📁 apps/learning_tracks/models.py

from django.db import models
from django.conf import settings

class LearningTrack(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    courses = models.ManyToManyField('courses.Course', related_name='learning_tracks')
    mentor = models.ForeignKey('mentors.MentorProfile', on_delete=models.CASCADE, related_name='learning_tracks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class TrackEnrollment(models.Model):
    track = models.ForeignKey(LearningTrack, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_completed = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('track', 'student')
