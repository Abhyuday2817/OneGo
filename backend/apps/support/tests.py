# support/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import SupportTicket

class SupportTicketTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='pass')
        self.client.force_authenticate(self.user)

    def test_create_support_ticket(self):
        data = {
            "subject": "Need help with booking",
            "message": "I can't book a session with mentor X.",
            "priority": "high"
        }
        response = self.client.post('/api/support/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SupportTicket.objects.count(), 1)

    def test_list_support_tickets(self):
        SupportTicket.objects.create(
            user=self.user,
            subject="Login issue",
            message="I can't login to my account.",
            priority="urgent"
        )
        response = self.client.get('/api/support/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_ticket_status(self):
        ticket = SupportTicket.objects.create(
            user=self.user,
            subject="Sample",
            message="Msg",
            priority="medium"
        )
        response = self.client.patch(f'/api/support/{ticket.id}/', {"status": "closed"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], "closed")
