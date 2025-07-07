from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.categories.models import Category
import logging
from datetime import datetime, time

logger = logging.getLogger(__name__)

class MentorProfileQuerySet(models.QuerySet):
    def top_rated(self, min_rating=4.0):
        return self.filter(rating__gte=min_rating).order_by('-rating', '-num_reviews')

    def available_at(self, dt):
        return self.filter(
            availability_windows__start__lte=dt,
            availability_windows__end__gte=dt,
        ).distinct()

    def with_stats(self):
        return self.prefetch_related(
            'specialties', 
            'availability_windows', 
            'weekly_availability',
            'user'
        )

class MentorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mentor_profile'
    )
    bio = models.TextField(blank=True, max_length=2000)
    specialties = models.ManyToManyField(Category, related_name='mentors')
    hourly_rate = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    per_minute_rate = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    num_reviews = models.PositiveIntegerField(default=0)
    certifications = models.TextField(blank=True, max_length=3000)
    languages = models.CharField(
        max_length=200, 
        blank=True, 
        help_text='Comma-separated ISO language codes (e.g. en, hi, fr)'
    )
    expertise = models.CharField(max_length=255, default='General')
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='mentors/photos/', blank=True, null=True)
    education = models.TextField(blank=True, max_length=2000)
    experience = models.TextField(blank=True, max_length=3000)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MentorProfileQuerySet.as_manager()

    class Meta:
        ordering = ['-rating', 'user__username']
        indexes = [
            models.Index(fields=['rating', 'is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} (⭐{self.rating:.1f})'

    def clean(self):
        if self.hourly_rate and self.per_minute_rate:
            if self.hourly_rate < self.per_minute_rate * 60:
                raise ValidationError('Hourly rate should be at least 60 times per-minute rate')

    def get_upcoming_sessions(self):
        try:
            from apps.sessions.models import Session
            return Session.objects.filter(mentor=self, start_time__gte=timezone.now())
        except ImportError:
            logger.warning("Session model not found")
            return []

    def total_earnings(self):
        try:
            from apps.sessions.models import Session
            qs = Session.objects.filter(mentor=self, status='completed', verified=True)
            result = qs.aggregate(total=models.Sum('rate_applied'))
            return result['total'] or 0
        except (ImportError, AttributeError):
            logger.warning("Unable to calculate earnings")
            return 0

    def total_students_taught(self):
        try:
            from apps.sessions.models import Session
            return Session.objects.filter(mentor=self).values('student').distinct().count()
        except ImportError:
            logger.warning("Session model not found")
            return 0

    def is_available(self, start, end):
        """
        Checks if the mentor is available for the given datetime range.
        """
        try:
            from apps.sessions.models import Session
            # All windows must cover requested time
            for win in self.availability_windows.all():
                if win.start <= start and win.end >= end:
                    # Check for session conflicts
                    conflict = Session.objects.filter(
                        mentor=self,
                        start_time__lt=end,
                        end_time__gt=start,
                        status__in=['scheduled', 'completed'],
                    ).exists()
                    return not conflict
            return False
        except ImportError:
            logger.warning("Session model not found")
            return False

    def weekly_availability_today(self):
        today = timezone.now().strftime('%a').lower()
        return self.weekly_availability.filter(day=today, is_available=True)

    def average_session_duration(self):
        try:
            from apps.sessions.models import Session
            sessions = Session.objects.filter(mentor=self, status='completed')
            durations = []
            for session in sessions:
                if session.end_time and session.start_time:
                    duration = (session.end_time - session.start_time).total_seconds()
                    durations.append(duration)
            if durations:
                avg_seconds = sum(durations) / len(durations)
                return avg_seconds / 60  # minutes
            return 0
        except ImportError:
            logger.warning("Session model not found")
            return 0

    def update_rating(self):
        """Update mentor rating based on reviews"""
        try:
            from apps.reviews.models import Review
            reviews = Review.objects.filter(mentor=self)
            if reviews.exists():
                avg_rating = reviews.aggregate(avg=models.Avg('rating'))['avg']
                self.rating = round(avg_rating, 1)
                self.num_reviews = reviews.count()
                self.save(update_fields=['rating', 'num_reviews'])
        except ImportError:
            pass

class AvailabilityWindow(models.Model):
    mentor = models.ForeignKey(
        MentorProfile, 
        related_name='availability_windows', 
        on_delete=models.CASCADE
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start']
        indexes = [
            models.Index(fields=['mentor', 'start', 'end']),
        ]

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('Start time must be before end time')
        if self.start <= timezone.now():
            raise ValidationError('Availability cannot be in the past')

    def __str__(self):
        return f"{self.mentor.user.username}: {self.start} → {self.end}"

class MentorAvailability(models.Model):
    WEEKDAYS = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]

    mentor = models.ForeignKey(
        MentorProfile, 
        related_name='weekly_availability', 
        on_delete=models.CASCADE
    )
    day = models.CharField(max_length=3, choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    timezone = models.CharField(max_length=100, default='Asia/Kolkata')
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('mentor', 'day', 'start_time', 'end_time')
        ordering = ['mentor', 'day', 'start_time']

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time')

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time}–{self.end_time} ({self.mentor.user.username})"

    def overlaps(self, check_time):
        """
        check_time: can be a datetime, time, or string
        Returns True if check_time is within this availability window
        """
        local_time = None
        # Convert check_time to a datetime.time object
        if isinstance(check_time, str):
            try:
                # Try HH:MM:SS or HH:MM
                try:
                    local_time = datetime.strptime(check_time, "%H:%M:%S").time()
                except ValueError:
                    local_time = datetime.strptime(check_time, "%H:%M").time()
            except Exception:
                # Try full ISO datetime string
                try:
                    dt = datetime.fromisoformat(check_time)
                    local_time = dt.astimezone(timezone.get_current_timezone()).time()
                except Exception:
                    raise TypeError("String time format should be 'HH:MM', 'HH:MM:SS', or ISODateTime string")
        elif isinstance(check_time, datetime):
            local_time = check_time.astimezone(timezone.get_current_timezone()).time()
        elif isinstance(check_time, time):
            local_time = check_time
        else:
            raise TypeError("overlaps expects a datetime, time, or string input.")

        return self.is_available and self.start_time <= local_time <= self.end_time