# apps/appointments/tests/test_models.py

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
from apps.mentors.models import MentorProfile
from apps.appointments.models import Appointment
from apps.categories.models import Category
from django.core.exceptions import ValidationError


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="student1", password="secret")
        self.mentor_user = User.objects.create_user(username="mentor1", password="secret")
        self.category = Category.objects.create(name="Data Science")

        self.mentor_profile = MentorProfile.objects.create(
            user=self.mentor_user,
            bio="Data mentor",
            hourly_rate=400,
            per_minute_rate=10,
            expertise="Data Science",
            rating=4.8,
            education="PhD in Stats",
            experience="10 years",
            languages="en",
        )
        self.mentor_profile.specialties.add(self.category)

        # Time: tomorrow 10–11 AM
        self.start_time = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        self.end_time = self.start_time + timedelta(hours=1)

        self.appt = Appointment.objects.create(
            student=self.student,
            mentor=self.mentor_profile,
            start_time=self.start_time,
            end_time=self.end_time,
        )

    def test_appointment_str(self):
        self.assertIn(self.student.username, str(self.appt))

    def test_duration_minutes(self):
        self.assertEqual(self.appt.duration().total_seconds(), 3600)

    def test_is_conflict_returns_true(self):
        conflict_appt = Appointment(
            student=self.student,
            mentor=self.mentor_profile,
            start_time=self.start_time,
            end_time=self.end_time + timedelta(minutes=30),
        )
        with self.assertRaises(ValidationError):
            conflict_appt.full_clean()

    def test_working_hours_check(self):
        invalid_appt = Appointment(
            student=self.student,
            mentor=self.mentor_profile,
            start_time=self.start_time.replace(hour=20),
            end_time=self.start_time.replace(hour=21),
        )
        with self.assertRaises(ValidationError) as e:
            invalid_appt.full_clean()
        self.assertIn("working hours", str(e.exception).lower())

    def test_reschedule_logic(self):
        new_start = self.start_time + timedelta(days=1)
        new_end = new_start + timedelta(minutes=45)
        self.appt.reschedule(new_start, new_end)
        self.assertEqual(self.appt.start_time, new_start)
        self.assertEqual(self.appt.status, "rescheduled")
