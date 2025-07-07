from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Category
from apps.mentors.models import MentorProfile
from apps.learning_tracks.models import LearningTrack

User = get_user_model()

class LearningTracksTestCase(APITestCase):
    def setUp(self):
        # Create mentor and student users
        self.mentor_user = User.objects.create_user(username="mentor", password="Mentor@123")
        self.student_user = User.objects.create_user(username="student", password="Student@123")

        # Create mentor profile with all required fields
        self.category = Category.objects.create(name="AI")
        self.mentor = MentorProfile.objects.create(
            user=self.mentor_user,
            bio="Expert AI mentor",
            hourly_rate=1000,
            per_minute_rate=10,  # ✅ Required now
            expertise="AI",
            availability_slots="9AM-5PM"
        )
        self.mentor.specialties.add(self.category)

        # Create course and learning track
        self.course = Course.objects.create(
            title="AI Basics",
            description="Learn AI from scratch",
            price=499,
            mentor=self.mentor,
            category=self.category,
            delivery_type="recorded",
            schedule_info="Anytime"
        )
        self.track = LearningTrack.objects.create(
            title="AI Learning Track",
            description="Track for aspiring AI learners",
            mentor=self.mentor
        )
        self.track.courses.add(self.course)

        # Login as student
        self.client.login(username="student", password="Student@123")

    def test_list_tracks(self):
        res = self.client.get("/api/learning-tracks/")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test_enroll_track(self):
        res = self.client.post("/api/track-enrollments/", {
            "track": self.track.id
        })
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["track"], self.track.id)
