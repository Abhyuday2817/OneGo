# mentors/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from categories.models import Category
from mentors.models import MentorProfile
from rest_framework.test import APIClient

User = get_user_model()

class MentorProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mentor1", password="pass123")
        self.category = Category.objects.create(name="Math", type="Education")
        self.mentor_profile = MentorProfile.objects.create(
            user=self.user,
            bio="Experienced math tutor",
            hourly_rate=100,
            per_minute_rate=2,
            rating=4.5,
            num_reviews=10,
            languages="en,hi",
            certifications="BSc Math"
        )
        self.mentor_profile.specialties.add(self.category)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_mentor_profile_str(self):
        self.assertEqual(str(self.mentor_profile), f"{self.user.username} (⭐{self.mentor_profile.rating:.1f})")

    def test_available_at_filter(self):
        now = "2025-06-20T12:00:00Z"
        self.mentor_profile.availability_windows = [
            {"start": "2025-06-20T10:00:00Z", "end": "2025-06-20T14:00:00Z"}
        ]
        self.mentor_profile.save()

        response = self.client.get(f"/api/mentors/?available_at={now}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_mentor_dashboard(self):
        response = self.client.get("/api/mentors/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("mentor", response.data)
        self.assertIn("total_earnings", response.data)

    def test_mentor_me_view(self):
        response = self.client.get("/api/mentors/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["id"], self.user.id)

    def test_update_mentor_profile(self):
        data = {"bio": "Updated bio", "specialty_ids": [self.category.id]}
        response = self.client.put("/api/mentors/me/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.mentor_profile.refresh_from_db()
        self.assertEqual(self.mentor_profile.bio, "Updated bio")
