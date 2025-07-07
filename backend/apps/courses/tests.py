# apps/courses/tests.py

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

from apps.courses.models import Course, Category
from apps.mentors.models import MentorProfile
from apps.enrollments.models import Enrollment

User = get_user_model()

class CoursesTestCase(APITestCase):
    def setUp(self):
        self.mentor_user = User.objects.create_user(username="mentor", password="Mentor@123")
        self.student_user = User.objects.create_user(username="student", password="Student@123")

        self.mentor = MentorProfile.objects.create(
            user=self.mentor_user,
            expertise="Python",
            hourly_rate=100,
            per_minute_rate=5,
            bio="Expert Python Mentor",
            languages="English",
            country="India",
            availability_slots="9AM-5PM",
        )

        self.category = Category.objects.create(name="Programming")

        self.course = Course.objects.create(
            title="Intro to Python",
            description="Learn Python basics",
            price=500,
            mentor=self.mentor,
            category=self.category,
            delivery_type="recorded",
            schedule_info="Anytime"
        )

        # Login student for auth-required APIs
        self.client.login(username="student", password="Student@123")

    def test_list_courses(self):
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_enroll_course(self):
        response = self.client.post(f"/api/courses/{self.course.id}/enroll/")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["course_id"], self.course.id)

    def test_enrollment_prevent_duplicate(self):
        # First enrollment
        self.client.post(f"/api/courses/{self.course.id}/enroll/")

        # Second enrollment (duplicate)
        duplicate = self.client.post(f"/api/courses/{self.course.id}/enroll/")
        print("Duplicate enroll response:", duplicate.status_code, duplicate.json())

        self.assertIn(duplicate.status_code, [400, 409])
        self.assertEqual(duplicate.json()["detail"], "Already enrolled.")

    def test_course_detail(self):
        response = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Intro to Python")

    def test_course_search_filter(self):
        response = self.client.get("/api/courses/?search=Python")
        self.assertEqual(response.status_code, 200)

        # Handle pagination if enabled
        course_list = response.data.get("results", response.data)

        self.assertTrue(any("Python" in c["title"] for c in course_list))
