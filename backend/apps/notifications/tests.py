from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification

class NotificationModelTest(TestCase):
    def test_create_notification(self):
        user = get_user_model().objects.create_user(username='testuser', password='pass')
        notif = Notification.objects.create(user=user, message="Hello!")
        self.assertIn("Notification", str(notif))

    def test_mark_as_read(self):
        user = get_user_model().objects.create_user(username='testuser2', password='pass')
        notif = Notification.objects.create(user=user, message="Test Read")
        notif.mark_as_read()
        self.assertTrue(notif.read)