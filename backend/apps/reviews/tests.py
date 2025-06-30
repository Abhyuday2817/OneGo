from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from mentors.models import MentorProfile
from .models import Review
from categories.models import Category

User = get_user_model()

class ReviewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(username='student', password='test123')
        self.mentor_user = User.objects.create_user(username='mentor', password='test123')
        self.category = Category.objects.create(name="Science", type="Education")
        self.mentor = MentorProfile.objects.create(
            user=self.mentor_user,
            hourly_rate=100,
            per_minute_rate=2,
            bio="Test mentor",
            rating=0,
        )
        self.mentor.specialties.add(self.category)
        self.review_url = '/api/reviews/'
        self.client.force_authenticate(user=self.student)

    def test_create_review(self):
        payload = {
            "reviewee_id": self.mentor.id,
            "rating": 5,
            "comment": "Excellent guidance"
        }
        response = self.client.post(self.review_url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().rating, 5)

    def test_get_review_list(self):
        Review.objects.create(reviewer=self.student, reviewee=self.mentor, rating=4, comment="Good")
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_review(self):
        review = Review.objects.create(reviewer=self.student, reviewee=self.mentor, rating=3, comment="Okay")
        update_url = f"{self.review_url}{review.id}/"
        response = self.client.patch(update_url, {"rating": 4}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["rating"], 4)

    def test_delete_review(self):
        review = Review.objects.create(reviewer=self.student, reviewee=self.mentor, rating=2)
        delete_url = f"{self.review_url}{review.id}/"
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Review.objects.count(), 0)

    def test_review_permission_denied_for_others(self):
        # Another user trying to edit someone else's review
        review = Review.objects.create(reviewer=self.student, reviewee=self.mentor, rating=4)
        another_user = User.objects.create_user(username='intruder', password='test456')
        self.client.force_authenticate(user=another_user)
        update_url = f"{self.review_url}{review.id}/"
        response = self.client.patch(update_url, {"rating": 1})
        self.assertIn(response.status_code, [403, 404])  # Forbidden or Not Found
