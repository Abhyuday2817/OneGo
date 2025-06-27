# appointments/tests/test_api.py

from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from doctors.models import DoctorProfile

class AppointmentAPITest(APITestCase):
    def setUp(self):
        # 1) Create a patient user
        self.patient = User.objects.create_user(username="bob", password="secret")

        # 2) Create a doctor user & profile
        doctor_user = User.objects.create_user(username="drsmith", password="secret")
        self.doctor_profile = DoctorProfile.objects.create(
            user=doctor_user,
            speciality="GP",
            available=True,
        )

        # 3) Obtain a JWT token (we’ll act as the patient)
        resp = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "bob", "password": "secret"},
            format="json",
        )
        self.token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_list_appointments_empty(self):
        """GET /api/appointments/ should return 200 and an empty paginated list."""
        url = reverse("appointments_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # DRF pagination wraps results under "results"
        self.assertIn("results", response.data)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(response.data["count"], 0)

    def test_create_appointment(self):
        """POST /api/appointments/ should create an appointment and return 201."""
        url = reverse("appointments_list_create")
        payload = {
            "doctor": self.doctor_profile.id,
            "patient": self.patient.id,
            "start_time": "2025-06-20T10:00:00Z",
            "end_time":   "2025-06-20T10:30:00Z",
        }
        response = self.client.post(url, payload, format="json")

        # If you still see 400, uncomment to inspect:
        # print("Validation errors:", response.data)

        self.assertEqual(response.status_code, 201)
        # verify the returned appointment
        self.assertIn("id", response.data)
        self.assertEqual(response.data["doctor"], self.doctor_profile.id)
        self.assertEqual(response.data["patient"], self.patient.id)
