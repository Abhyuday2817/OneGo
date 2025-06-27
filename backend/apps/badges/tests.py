from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Badge, UserBadge
from .services import award_badge

User = get_user_model()

class BadgeAwardingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234")
        self.badge = Badge.objects.create(slug="test-badge", name="Test Badge", description="A test badge")

    def test_award_badge(self):
        awarded = award_badge(self.user, "test-badge")
        self.assertTrue(awarded)
        self.assertEqual(UserBadge.objects.filter(user=self.user).count(), 1)

    def test_duplicate_award(self):
        award_badge(self.user, "test-badge")
        awarded_again = award_badge(self.user, "test-badge")
        self.assertFalse(awarded_again)  # shouldn't award duplicate

    def test_badge_str(self):
        self.assertEqual(str(self.badge), "Test Badge")
