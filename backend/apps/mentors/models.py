from django.db import models
from django.conf import settings
from django.utils import timezone
from django.apps import apps

from apps.categories.models import Category


class MentorProfileQuerySet(models.QuerySet):
    def top_rated(self, min_rating=4.0):
        return self.filter(rating__gte=min_rating).order_by('-rating', '-num_reviews')

    def available_at(self, dt):
        return self.filter(
            availability_windows__start__lte=dt,
            availability_windows__end__gte=dt,
        ).distinct()


class MentorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mentor_profile'
    )
    bio = models.TextField(blank=True)
    specialties = models.ManyToManyField(Category, related_name='mentors')
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    per_minute_rate = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.FloatField(default=0)
    num_reviews = models.PositiveIntegerField(default=0)
    certifications = models.TextField(blank=True)
    languages = models.CharField(
        max_length=200,
        blank=True,
        help_text='Comma-separated ISO language codes (e.g. en, hi, fr)'
    )
    expertise = models.CharField(max_length=255, default='General')
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MentorProfileQuerySet.as_manager()

    class Meta:
        ordering = ['-rating', 'user__username']

    def __str__(self):
        return f'{self.user.username} (⭐{self.rating:.1f})'

    def get_upcoming_sessions(self):
        Session = apps.get_model('sessions', 'Session')
        return Session.objects.filter(mentor=self, start_time__gte=timezone.now())

    def total_earnings(self):
        Session = apps.get_model('sessions', 'Session')
        qs = Session.objects.filter(
            mentor=self,
            status=Session.STATUS_COMPLETED,
            verified=True,
        )
        return qs.aggregate(models.Sum('rate_applied'))['rate_applied__sum'] or 0

    def is_available(self, start, end):
        for win in self.availability_windows.all():
            if win.start <= start and win.end >= end:
                Session = apps.get_model('sessions', 'Session')
                conflict = Session.objects.filter(
                    mentor=self,
                    start_time__lt=end,
                    end_time__gt=start,
                    status__in=[Session.STATUS_SCHEDULED, Session.STATUS_COMPLETED],
                ).exists()
                return not conflict
        return False

class AvailabilityWindow(models.Model):
    mentor = models.ForeignKey(
        MentorProfile,
        related_name='availability_windows',
        on_delete=models.CASCADE
    )
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        ordering = ['start']

    def __str__(self):
        return f"{self.mentor.user.username}: {self.start} → {self.end}"
