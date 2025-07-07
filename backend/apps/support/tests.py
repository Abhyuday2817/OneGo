from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.support.models import SupportTicket

User = get_user_model()

class SupportTicketTestCase(APITestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="student", password="Test@123")
        self.admin = User.objects.create_user(username="admin", password="Admin@123", is_staff=True)

    def test_create_ticket(self):
        self.client.login(username="student", password="Test@123")
        response = self.client.post("/api/support/", {
            "subject": "Issue 1",
            "message": "Something broke",
            "priority": "high"
        })
        print("Create Ticket:", response.status_code, response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["status"], "open")

    def test_ticket_lifecycle(self):
        # 🔹 Step 1: Create a ticket
        self.client.login(username="student", password="Test@123")
        res = self.client.post("/api/support/", {
            "subject": "Issue 2",
            "message": "Test Message",
            "priority": "medium"
        })
        print("Ticket Create:", res.status_code, res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", res.data)
        ticket_id = res.data["id"]
        self.client.logout()

        # 🔹 Step 2: Assign ticket (as admin)
        self.client.login(username="admin", password="Admin@123")
        assign = self.client.post(f"/api/support/{ticket_id}/assign/", {
            "assigned_to": self.admin.id
        })
        print("Assign Ticket:", assign.status_code, assign.data)
        self.assertEqual(assign.status_code, 200)

        # 🔹 Step 3: Close ticket
        close = self.client.post(f"/api/support/{ticket_id}/close/", {
            "resolution": "Resolved it."
        })
        print("Close Ticket:", close.status_code, close.data)
        self.assertEqual(close.status_code, 200)

        # 🔹 Step 4: Check admin stats
        stats = self.client.get("/api/support/stats/")
        print("Ticket Stats:", stats.status_code, stats.data)
        self.assertEqual(stats.status_code, 200)
        self.assertIn("status_counts", stats.data)
