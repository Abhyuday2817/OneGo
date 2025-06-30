from django.test import TestCase
from apps.users.models import User
from apps.mentors.models import MentorProfile
from .models import MentorReview


class MentorReviewTestCase(TestCase):
    def setUp(self):
        self.student = User.objects.create(username='student1', email='student1@example.com')
        self.mentor_user = User.objects.create(username='mentor1', email='mentor1@example.com')
        self.mentor_profile = MentorProfile.objects.create(user=self.mentor_user, expertise='Python, AI')

    def test_create_review(self):
        review = MentorReview.objects.create(
            mentor=self.mentor_profile,
            student=self.student,
            rating=5,
            review="Excellent mentoring session!"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.mentor, self.mentor_profile)
        self.assertEqual(review.student, self.student)