# onego/backend/services/escrow.py

from django.db import transaction
from apps.payments.models import Wallet

def hold_session_fee(student, session, reference=""):
    """
    When booking: move `session.rate_applied * duration` from student's wallet to escrow.
    """
    wallet = Wallet.objects.get(user=student)
    total = session.duration_minutes() * session.rate_applied
    wallet.hold_in_escrow(total, reference=f"{reference or 'session'}-{session.pk}")

def release_to_mentor(session, reference=""):
    """
    On session completion: release escrowed funds to mentor's available balance.
    """
    student_wallet = Wallet.objects.get(user=session.student)
    mentor_wallet  = Wallet.objects.get(user=session.mentor.user)
    total = session.duration_minutes() * session.rate_applied
    with transaction.atomic():
        student_wallet.release_escrow(total, reference=f"release-session-{session.pk}")
        mentor_wallet.deposit(total, reference=f"payout-session-{session.pk}")

def refund_session(session, reference=""):
    """
    On cancellation: refund escrow back to student.
    """
    wallet = Wallet.objects.get(user=session.student)
    total  = session.duration_minutes() * session.rate_applied
    wallet.release_escrow(total, reference=f"refund-session-{session.pk}")
