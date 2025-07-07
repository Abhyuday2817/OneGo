from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.wallets.models import Wallet
from apps.payments.models import Payment
from decimal import Decimal

User = get_user_model()

class PaymentsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="payer", password="Pay@123")
        self.client.login(username="payer", password="Pay@123")

    def test_checkout_payment(self):
        res = self.client.post("/api/payments/checkout/", {
            "amount": 100,
            "method": "razorpay"
        })
        self.assertIn(res.status_code, [200, 201])
        self.assertIn("order_id", res.data)

    def test_payment_model_behavior(self):
        payment = Payment.objects.create(user=self.user, amount=Decimal("100.00"), status="pending")
        self.assertEqual(str(payment), f"{self.user} - 100.00 - pending")
        self.assertFalse(payment.is_successful())

        payment.status = "completed"
        payment.save()
        self.assertTrue(payment.is_successful())
