from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.mentors.models import MentorProfile
from apps.sessions.models import Session

User = get_user_model()


class SessionTestCase(APITestCase):
    def setUp(self):
        self.mentor_user = User.objects.create_user(username="mentor", password="mentorpass")
        self.student_user = User.objects.create_user(username="student", password="studentpass")

        self.mentor = MentorProfile.objects.create(
            user=self.mentor_user,
            expertise="Python",
            hourly_rate=100,
            per_minute_rate=5,
            bio="Experienced Python Mentor",
            languages="English",
            country="India",
            availability_slots="9AM-5PM"
        )

        self.session = Session.objects.create(
            student=self.student_user,
            mentor=self.mentor,
            session_type=Session.TYPE_FIXED,
            start_time=timezone.now() + timedelta(hours=2),
            end_time=timezone.now() + timedelta(hours=3),
            rate_applied=100
        )

        self.client.login(username="student", password="studentpass")

    def test_create_session(self):
        self.client.logout()
        self.client.login(username="student", password="studentpass")
        data = {
            "student_id": self.student_user.id,
            "mentor_id": self.mentor.id,
            "session_type": Session.TYPE_FIXED,
            "start_time": (timezone.now() + timedelta(days=1)).isoformat(),
            "end_time": (timezone.now() + timedelta(days=1, hours=1)).isoformat(),
            "rate_applied": 150
        }
        response = self.client.post("/api/sessions/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)

    def test_confirm_by_student(self):
        response = self.client.post(f"/api/sessions/{self.session.id}/confirm/?role=student")
        self.assertEqual(response.status_code, 200)
        self.session.refresh_from_db()
        self.assertTrue(self.session.student_confirmed)

    def test_confirm_by_mentor(self):
        self.client.logout()
        self.client.login(username="mentor", password="mentorpass")
        response = self.client.post(f"/api/sessions/{self.session.id}/confirm/?role=mentor")
        self.assertEqual(response.status_code, 200)
        self.session.refresh_from_db()
        self.assertTrue(self.session.mentor_confirmed)

    def test_cancel_session_by_student(self):
        response = self.client.post(f"/api/sessions/{self.session.id}/cancel/")
        self.assertEqual(response.status_code, 200)
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, Session.STATUS_CANCELLED)

    def test_start_end_session_by_mentor(self):
        self.client.logout()
        self.client.login(username="mentor", password="mentorpass")
        # Start session
        response = self.client.post(f"/api/sessions/{self.session.id}/start/")
        self.assertEqual(response.status_code, 200)
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, Session.STATUS_ONGOING)

        # End session
        response = self.client.post(f"/api/sessions/{self.session.id}/end/")
        self.assertEqual(response.status_code, 200)
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, Session.STATUS_COMPLETED)
        self.assertIsNotNone(self.session.total_price)

    def test_stats(self):
        response = self.client.get("/api/sessions/stats/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_sessions", response.data)

    def test_bulk_cancel(self):
        s2 = Session.objects.create(
            student=self.student_user,
            mentor=self.mentor,
            session_type=Session.TYPE_FIXED,
            start_time=timezone.now() + timedelta(hours=4),
            end_time=timezone.now() + timedelta(hours=5),
            rate_applied=200
        )
        response = self.client.post("/api/sessions/bulk_cancel/", {"ids": [self.session.id, s2.id]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["cancelled_count"], 2)
