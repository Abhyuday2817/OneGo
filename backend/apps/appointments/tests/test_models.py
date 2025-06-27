from django.test import TestCase
from appointments.models import Appointment
from users.models import User
from doctors.models import DoctorProfile
from django.utils import timezone

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="patient")
        self.doctor_user = User.objects.create(username="doctor")
        self.doctor = DoctorProfile.objects.create(user=self.doctor_user, speciality="GP", available=True)
        self.appt = Appointment.objects.create(
            patient=self.user,
            doctor=self.doctor,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_duration(self):
        self.assertEqual(self.appt.duration(), timezone.timedelta(hours=1))

    def test_str(self):
        self.assertIn("patient", str(self.appt))

    def test_conflict_detection(self):
        # Overlapping appointment
        conflict = Appointment(
            patient=self.user,
            doctor=self.doctor,
            start_time=self.appt.start_time,
            end_time=self.appt.end_time + timezone.timedelta(minutes=30)
        )
        with self.assertRaises(Exception):
            conflict.full_clean()