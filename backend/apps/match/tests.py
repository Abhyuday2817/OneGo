from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from categories.models import Category
from mentors.models import MentorProfile
from courses.models import Course
from enrollments.models import Enrollment

class MatchAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create student, mentors, courses, enrollments, etc.
        self.student = User.objects.create_user("stud", "s@e.com", "pass")
        self.client.force_authenticate(self.student)
        # …more setup…

    def test_recommend_merits_from_enrollments(self):
        resp = self.client.get("/api/match/courses/?limit=2")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)
