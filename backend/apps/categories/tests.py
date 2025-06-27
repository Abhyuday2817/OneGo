from django.test import TestCase
from .models import Category

class CategoryTestCase(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(
            name="Data Science",
            type=Category.TYPE_EDUCATION,
            description="All things data"
        )

    def test_category_str(self):
        self.assertEqual(str(self.cat), "Data Science (Education)")

    def test_top_courses_returns_empty(self):
        top_courses = self.cat.top_courses()
        self.assertEqual(top_courses.count(), 0)
