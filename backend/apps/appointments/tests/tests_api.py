# apps/appointments/tests/test_api.py

from django.urls import reverse
from rest_framework.test import APITestCase
from apps.users.models import User
from apps.mentors.models import MentorProfile
from apps.categories.models import Category
from rest_framework import status
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class AppointmentAPITestCase(APITestCase):

    def setUp(self):
        # Create a student
        self.student = User.objects.create_user(username="bob", password="secret")

        # Create a mentor + mentor profile
        self.mentor_user = User.objects.create_user(username="mentor1", password="secret")
        self.category = Category.objects.create(name="AI")
        self.mentor_profile = MentorProfile.objects.create(
            user=self.mentor_user,
            bio="AI Expert",
            hourly_rate=300,
            per_minute_rate=5,
            expertise="ML",
            education="MS in ML",
            experience="5 years",
            languages="en,hi",
        )
        self.mentor_profile.specialties.add(self.category)

        # Get JWT token for student
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "bob", "password": "secret"},
            format="json"
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_list_appointments_should_be_empty(self):
        """GET /api/appointments/ should return empty result initially"""
        response = self.client.get("/api/appointments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
        self.assertIsInstance(response.data["results"], list)

    def test_create_appointment_should_work(self):
        """POST /api/appointments/ should create an appointment"""
        tomorrow = make_aware(datetime.now() + timedelta(days=1))
        start = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
        end = start + timedelta(minutes=30)

        response = self.client.post("/api/appointments/", {
            "mentor": self.mentor_profile.id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "notes": "Discuss AI roadmap"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["mentor"], self.mentor_profile.id)
