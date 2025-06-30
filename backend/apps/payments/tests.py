from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Payment
from decimal import Decimal

class PaymentModelTest(TestCase):
    def test_create_payment(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        payment = Payment.objects.create(user=user, amount=Decimal("100.00"), status='pending')
        self.assertEqual(str(payment), f"{user} - 100.00 - pending")
        self.assertFalse(payment.is_successful())
        payment.status = "completed"
        payment.save()
        self.assertTrue(payment.is_successful())