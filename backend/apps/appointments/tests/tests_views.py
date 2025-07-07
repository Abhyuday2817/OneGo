# apps/appointments/tests/test_views.py

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.mentors.models import MentorProfile
from apps.categories.models import Category
from django.utils import timezone
from datetime import datetime, timedelta, time

User = get_user_model()


class AppointmentViewTests(APITestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="student1", password="Student@123")
        self.mentor_user = User.objects.create_user(username="mentor1", password="Mentor@123")
        self.category = Category.objects.create(name="AI")

        self.mentor = MentorProfile.objects.create(
            user=self.mentor_user,
            bio="AI mentor",
            hourly_rate=400,
            per_minute_rate=7,
            expertise="AI",
            rating=4.9,
            education="M.Tech AI",
            experience="6 years",
            languages="en,hi"
        )
        self.mentor.specialties.add(self.category)

        tomorrow = timezone.now().date() + timedelta(days=1)
        self.start_time = timezone.make_aware(datetime.combine(tomorrow, time(10, 0)))
        self.end_time = timezone.make_aware(datetime.combine(tomorrow, time(11, 0)))

        self.client.login(username="student1", password="Student@123")

    def test_create_appointment_success(self):
        response = self.client.post("/api/appointments/", {
            "mentor": self.mentor.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat()
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["mentor"], self.mentor.id)
    def test_create_conflicting_appointment_fails(self):
        # Create the first appointment
        self.client.post("/api/appointments/", {
            "mentor": self.mentor.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat()
        })

        # Try to create a conflicting one
        response = self.client.post("/api/appointments/", {
            "mentor": self.mentor.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat()
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)
        
    def test_appointment_outside_working_hours_fails(self):
        early = timezone.make_aware(datetime.combine(timezone.now().date() + timedelta(days=1), time(7, 0)))
        late = timezone.make_aware(datetime.combine(timezone.now().date() + timedelta(days=1), time(8, 0)))

        response = None
        try:
            response = self.client.post("/api/appointments/", {
                "mentor": self.mentor.id,
                "start_time": early.isoformat(),
                "end_time": late.isoformat()
            })
        except Exception as e:
            self.fail(f"Request raised an exception instead of returning 400: {e}")

        self.assertEqual(response.status_code, 400)

        # Check if working hours message is in any error field
        all_errors = []
        for field, errors in response.data.items():
            all_errors.extend(errors)

        self.assertTrue(
            any("working hours" in msg.lower() for msg in all_errors),
            f"Expected working hours error message, got: {response.data}"
        )




    def test_end_time_before_start_time(self):
        invalid_end = self.start_time - timedelta(minutes=10)
        response = self.client.post("/api/appointments/", {
            "mentor": self.mentor.id,
            "start_time": self.start_time.isoformat(),
            "end_time": invalid_end.isoformat()
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)
