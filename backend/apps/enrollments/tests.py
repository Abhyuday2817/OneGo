# apps/enrollments/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Course
from mentors.models import MentorProfile
from categories.models import Category
from .models import Enrollment

class EnrollmentModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.student = User.objects.create_user(username='student', password='test')
        self.mentor_user = User.objects.create_user(username='mentor', password='test')
        self.category = Category.objects.create(name="Math", type="Education")
        self.mentor = MentorProfile.objects.create(user=self.mentor_user)
        self.course = Course.objects.create(
            title="Algebra Basics",
            description="Intro to algebra",
            category=self.category,
            price=99.99,
            delivery_type="Live",
            mentor=self.mentor
        )
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course)

    def test_progress_percent_empty(self):
        self.assertEqual(self.enrollment.progress_percent, 0)

    def test_mark_complete_sets_progress(self):
        self.enrollment.progress = {"ch1": 50, "ch2": 80}
        self.enrollment.mark_complete()
        self.assertTrue(self.enrollment.completed)
        self.assertTrue(all(v == 100 for v in self.enrollment.progress.values()))

    def test_update_progress_marks_complete(self):
        self.enrollment.update_progress("intro", 100)
        self.assertFalse(self.enrollment.completed)
        self.enrollment.update_progress("module2", 100)
        self.assertTrue(self.enrollment.completed)
