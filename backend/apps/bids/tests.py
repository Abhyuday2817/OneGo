from django.test import TestCase
from django.contrib.auth import get_user_model
from gigs.models import GigRequest
from mentors.models import MentorProfile
from .models import Bid

User = get_user_model()

class BidTestCase(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="student1", password="pass")
        self.mentor_user = User.objects.create_user(username="mentor1", password="pass")
        self.mentor = MentorProfile.objects.create(user=self.mentor_user)
        self.gig = GigRequest.objects.create(
            student=self.student,
            title="Test Gig",
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
            proposal_text="Here’s my bid."
        )
        self.assertEqual(bid.status, Bid.STATUS_PENDING)

    def test_accept_bid(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor,
            proposed_rate=200,
            proposal_text="Accept me!"
        )
        bid.accept()
        self.assertEqual(bid.status, Bid.STATUS_ACCEPTED)
        self.assertEqual(
            Bid.objects.filter(status=Bid.STATUS_REJECTED).count(), 0
        )

    def test_reject_bid(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor,
            proposed_rate=300,
            proposal_text="Reject me?"
        )
        bid.reject()
        self.assertEqual(bid.status, Bid.STATUS_REJECTED)
