from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.mentors.models import MentorProfile, AvailabilitySlot

User = get_user_model()

class MentorTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="mentor1",
            email="mentor1@example.com",
            password="testpass123",
            role="mentor"
        )
        self.mentor_profile = MentorProfile.objects.create(
            user=self.user,
            bio="Expert in Python",
            expertise="Python, Django",
            hourly_rate=50
        )
        self.client.login(username="mentor1", password="testpass123")

    def test_get_my_mentor_profile(self):
        url = reverse("mentor-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["bio"], "Expert in Python")

    def test_partial_update_mentor_profile(self):
        url = reverse("mentor-me")
        data = {"bio": "Updated bio", "hourly_rate": 60}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["bio"], "Updated bio")
        self.assertEqual(response.data["hourly_rate"], 60)

    def test_get_weekly_availability(self):
        url = reverse("mentor-availability")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_availability_slot(self):
        url = reverse("mentor-availability")
        data = {
            "day": "monday",
            "start_time": "10:00:00",
            "end_time": "12:00:00"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(AvailabilitySlot.objects.filter(mentor=self.mentor_profile).exists())

    def test_dashboard_summary(self):
        url = reverse("mentor-dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_sessions", response.data)
        self.assertIn("total_earnings", response.data)
        self.assertIn("average_rating", response.data)

