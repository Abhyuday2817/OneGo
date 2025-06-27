# apps/consultations/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from mentors.models import MentorProfile
from .models import Consultation

User = get_user_model()

class ConsultationModelTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student1', password='test1234')
        self.mentor_user = User.objects.create_user(username='mentor1', password='test1234')
        self.mentor = MentorProfile.objects.create(user=self.mentor_user)
        self.time = timezone.now() + timezone.timedelta(days=1)

    def test_create_consultation(self):
        cons = Consultation.objects.create(
            student=self.student,
            mentor=self.mentor,
            topic="Test Topic",
            description="Test Desc",
            scheduled_time=self.time,
            duration_mins=30
        )
        self.assertEqual(cons.topic, "Test Topic")
        self.assertEqual(cons.status, Consultation.STATUS_SCHEDULED)

    def test_can_join(self):
        cons = Consultation.objects.create(
            student=self.student,
            mentor=self.mentor,
            topic="Join Test",
            scheduled_time=self.time,
            duration_mins=30
        )
        self.assertFalse(cons.can_join(self.student))  # too early

    def test_start_and_complete(self):
        cons = Consultation.objects.create(
            student=self.student,
            mentor=self.mentor,
            topic="Session Test",
            scheduled_time=self.time,
            duration_mins=30
        )
        cons.start("test_sid_123")
        self.assertEqual(cons.status, Consultation.STATUS_IN_PROGRESS)
        self.assertEqual(cons.twilio_room_sid, "test_sid_123")

        cons.complete("https://recording.url/sample.mp4")
        self.assertEqual(cons.status, Consultation.STATUS_COMPLETED)
        self.assertTrue(cons.recording_url)

    def test_cancel(self):
        cons = Consultation.objects.create(
            student=self.student,
            mentor=self.mentor,
            topic="Cancel Test",
            scheduled_time=self.time,
            duration_mins=30
        )
        cons.cancel()
        self.assertEqual(cons.status, Consultation.STATUS_CANCELLED)

# apps/consultations/admin.py
from django.contrib import admin
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "topic", "mentor", "student", "scheduled_time",
        "duration_mins", "status", "twilio_room_sid"
    )
    list_filter = ("status", "scheduled_time", "mentor")
    search_fields = ("topic", "student__username", "mentor__user__username")
    readonly_fields = ("created_at", "updated_at", "twilio_room_sid", "recording_url")