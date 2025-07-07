from django.test import TestCase
from .models import Category
from apps.courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Data Science",
            type=Category.TYPE_EDUCATION,
            description="All things data"
        )

        self.mentor = User.objects.create_user(username="mentor1", email="m@example.com", password="pass")
        # Create some dummy courses for testing
        Course.objects.create(title="ML 101", price=0, category=self.category, mentor=self.mentor)
        Course.objects.create(title="Deep Learning", price=199.99, category=self.category, mentor=self.mentor)
        Course.objects.create(title="Python for DS", price=99.99, category=self.category, mentor=self.mentor)

    def test_category_str(self):
        self.assertEqual(str(self.category), "Data Science (Education)")

    def test_top_courses_returns_limited(self):
        top_courses = self.category.top_courses(limit=2)
        self.assertEqual(top_courses.count(), 2)
        self.assertTrue(top_courses[0].price >= top_courses[1].price)

    def test_has_free_courses(self):
        self.assertTrue(self.category.has_free_courses())

    def test_total_courses(self):
        self.assertEqual(self.category.total_courses(), 3)

    def test_average_price(self):
        avg = self.category.average_price()
        self.assertAlmostEqual(avg, (0 + 199.99 + 99.99) / 3, places=2)

    def test_by_type_filter(self):
        categories = Category.objects.by_type(Category.TYPE_EDUCATION)
        self.assertIn(self.category, categories)

    def test_top_categories_queryset(self):
        top = Category.objects.top_categories()
        self.assertGreaterEqual(len(top), 1)
        self.assertEqual(top[0], self.category)
