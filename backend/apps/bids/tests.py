from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.gigs.models import GigRequest
from apps.mentors.models import MentorProfile
from .models import Bid

User = get_user_model()

class BidTestCase(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="student1", password="pass")
        self.mentor_user = User.objects.create_user(username="mentor1", password="pass")
        self.mentor = MentorProfile.objects.create(
            user=self.mentor_user,
            hourly_rate=500,
            per_minute_rate=10
        )
        self.gig = GigRequest.objects.create(
            student=self.student,
            title="Build a Django App",
            description="Need a basic mentor-student app",
            budget_min=100,
            budget_max=500,
            deadline="2099-12-31",
            status="Open"
        )

    def test_create_bid(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor,
            proposed_rate=200,
            proposal_text="I can do this project efficiently."
        )
        self.assertEqual(bid.status, Bid.STATUS_PENDING)
        self.assertEqual(str(bid), f"Bid #{bid.pk} by {self.mentor.user.username} on Gig #{self.gig.pk}")

    def test_bid_clean_validation(self):
        self.gig.status = "Closed"
        self.gig.save()
        bid = Bid(
            gig_request=self.gig,
            mentor=self.mentor,
            proposed_rate=300,
            proposal_text="Should fail"
        )
        with self.assertRaises(ValidationError):
            bid.clean()

    def test_accept_bid(self):
        other_mentor_user = User.objects.create_user(username="mentor2", password="pass")
        other_mentor = MentorProfile.objects.create(user=other_mentor_user, hourly_rate=500, per_minute_rate=10)
        bid1 = Bid.objects.create(gig_request=self.gig, mentor=self.mentor, proposed_rate=250, proposal_text="Pick me!")
        bid2 = Bid.objects.create(gig_request=self.gig, mentor=other_mentor, proposed_rate=300, proposal_text="Me too!")

        bid1.accept()
        bid1.refresh_from_db()
        bid2.refresh_from_db()

        self.assertEqual(bid1.status, Bid.STATUS_ACCEPTED)
        self.assertEqual(bid2.status, Bid.STATUS_REJECTED)

    def test_reject_bid(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor,
            proposed_rate=400,
            proposal_text="Don't pick me"
        )
        bid.reject()
        bid.refresh_from_db()
        self.assertEqual(bid.status, Bid.STATUS_REJECTED)

    def test_bid_rate_out_of_bounds(self):
        bid = Bid(
            gig_request=self.gig,
            mentor=self.mentor,
            proposed_rate=600,
            proposal_text="Too expensive"
        )
        with self.assertRaises(ValidationError):
            bid.full_clean()

    def test_is_status_helpers(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor,
            proposed_rate=150,
            proposal_text="Helper status test"
        )
        self.assertTrue(bid.is_pending())
        bid.accept()
        self.assertTrue(bid.is_accepted())
        bid.reject()
        self.assertTrue(bid.is_rejected())
