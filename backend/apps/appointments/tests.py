from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import User
from mentors.models import MentorProfile
from .models import Appointment
from datetime import timedelta

class AppointmentModelTest(TestCase):
    def setUp(self):
        # Create a student user & profile
        self.student_user = User.objects.create_user(
            username='student1', email='s1@example.com', password='testpass'
        )
        # Create a mentor user & profile
        self.mentor_user = User.objects.create_user(
            username='mentor1', email='m1@example.com', password='testpass'
        )
        self.mentor = MentorProfile.objects.create(
            user=self.mentor_user,
            bio='Expert in testing',
            hourly_rate=50,
            per_minute_rate=1,
            rating=0
        )

        # Define a valid future window
        self.start = timezone.now() + timedelta(days=1)
        self.end   = self.start + timedelta(hours=1)

    def test_default_status_and_conflict(self):
        """Creating an appointment should default to pending and have no conflicts."""
        appt = Appointment.objects.create(
            student=self.student_user,
            mentor=self.mentor,
            start_time=self.start,
            end_time=self.end
        )
        self.assertEqual(appt.status, Appointment.STATUS_PENDING)
        self.assertFalse(appt.is_conflict())

    def test_cancel_changes_status(self):
        """Calling cancel() sets status to canceled."""
        appt = Appointment.objects.create(
            student=self.student_user,
            mentor=self.mentor,
            start_time=self.start,
            end_time=self.end
        )
        appt.cancel()
        self.assertEqual(appt.status, Appointment.STATUS_CANCELED)

    def test_invalid_time_order_raises_validation(self):
        """start_time ≥ end_time should trigger validation error."""
        bad = Appointment(
            student=self.student_user,
            mentor=self.mentor,
            start_time=self.end,
            end_time=self.start
        )
        with self.assertRaises(ValidationError):
            bad.full_clean()

    def test_conflict_detection(self):
        """Overlapping appointments for the same mentor should be flagged."""
        # First one
        Appointment.objects.create(
            student=self.student_user,
            mentor=self.mentor,
            start_time=self.start,
            end_time=self.end
        )
        # A second overlapping window
        overlap_start = self.start + timedelta(minutes=30)
        overlap_end   = overlap_start + timedelta(hours=1)
        appt2 = Appointment(
            student=self.student_user,
            mentor=self.mentor,
            start_time=overlap_start,
            end_time=overlap_end
        )
        self.assertTrue(appt2.is_conflict())
