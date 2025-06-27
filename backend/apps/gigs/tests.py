# File: apps/gigs/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from categories.models import Category
from mentors.models import MentorProfile
from gigs.models import GigRequest, Bid, Contract
from datetime import timedelta

User = get_user_model()

class GigFlowTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username="student", password="test")
        self.mentor_user = User.objects.create_user(username="mentor", password="test")
        self.mentor_profile = MentorProfile.objects.create(user=self.mentor_user)
        self.category = Category.objects.create(name="Math", type="Education")
        self.gig = GigRequest.objects.create(
            student=self.student,
            category=self.category,
            title="Need help with algebra",
            description="Looking for weekly sessions",
            budget_min=100,
            budget_max=200,
            bidding_deadline=timezone.now() + timedelta(days=2)
        )

    def test_gig_creation(self):
        self.assertEqual(self.gig.title, "Need help with algebra")
        self.assertTrue(self.gig.is_open())

    def test_bid_placement(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor_profile,
            proposed_rate=150,
            proposal_text="I can help you with this."
        )
        self.assertEqual(bid.status, Bid.STATUS_PENDING)
        self.assertEqual(bid.mentor, self.mentor_profile)

    def test_bid_acceptance_and_contract(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor_profile,
            proposed_rate=180,
            proposal_text="Let’s start next week."
        )
        bid.accept()
        bid.refresh_from_db()
        self.assertEqual(bid.status, Bid.STATUS_ACCEPTED)
        self.assertTrue(hasattr(bid, "contract"))
        self.assertEqual(bid.contract.status, Contract.STATUS_ACTIVE)

    def test_bid_rejection(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor_profile,
            proposed_rate=180,
            proposal_text="Interested"
        )
        bid.reject()
        bid.refresh_from_db()
        self.assertEqual(bid.status, Bid.STATUS_REJECTED)

    def test_contract_completion(self):
        bid = Bid.objects.create(
            gig_request=self.gig,
            mentor=self.mentor_profile,
            proposed_rate=180,
            proposal_text="Let’s work"
        )
        bid.accept()
        contract = bid.contract
        contract.complete()
        contract.refresh_from_db()
        self.assertEqual(contract.status, Contract.STATUS_COMPLETED)
