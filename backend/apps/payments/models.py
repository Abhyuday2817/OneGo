from decimal import Decimal
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.users.models import User  # Ensure this import matches your project structure

class Transaction(models.Model):
    """
    Immutable ledger entry for all wallet and escrow movements:
      • deposit       – adding funds
      • withdraw      – removing funds
      • escrow_hold   – moving funds into escrow
      • escrow_release– releasing funds from escrow
    """
    TYPE_DEPOSIT        = "deposit"
    TYPE_WITHDRAW       = "withdraw"
    TYPE_ESCROW_HOLD    = "escrow_hold"
    TYPE_ESCROW_RELEASE = "escrow_release"

    TYPE_CHOICES = [
        (TYPE_DEPOSIT,        "Deposit"),
        (TYPE_WITHDRAW,       "Withdraw"),
        (TYPE_ESCROW_HOLD,    "Escrow Hold"),
        (TYPE_ESCROW_RELEASE, "Escrow Release"),
    ]

    user      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    amount    = models.DecimalField(max_digits=12, decimal_places=2)
    txn_type  = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reference = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional reference (e.g. session#123, refund-456)"
    )
    metadata  = models.JSONField(
        default=dict,
        blank=True,
        help_text="Extra data (e.g. { 'order_id': 'XYZ' })"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "txn_type", "timestamp"]),
        ]

    def __str__(self):
        sign = "+" if self.txn_type in (self.TYPE_DEPOSIT, self.TYPE_ESCROW_RELEASE) else "-"
        return f"{self.user.username} {self.txn_type} {sign}{abs(self.amount):.2f}"


class Wallet(models.Model):
    """
    A user wallet that tracks:
      • balance    – immediately available funds
      • escrowed   – funds held pending completion/refund
    Provides methods to deposit, withdraw, hold and release funds,
    each of which creates a corresponding Transaction entry.
    """
    user     = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet"
    )
    balance  = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Available balance"
    )
    escrowed = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Funds currently held in escrow"
    )

    class Meta:
        verbose_name_plural = "Wallets"

    def __str__(self):
        return (
            f"{self.user.username}: balance={self.balance:.2f} "
            f"(escrowed={self.escrowed:.2f})"
        )

    def _record(self, amount, txn_type, reference="", metadata=None):
        Transaction.objects.create(
            user=self.user,
            amount=amount,
            txn_type=txn_type,
            reference=reference,
            metadata=metadata or {}
        )

    def deposit(self, amount, reference="", metadata=None):
        """Add positive funds to balance."""
        amt = Decimal(amount)
        if amt <= 0:
            raise ValidationError("Deposit amount must be positive.")
        self.balance += amt
        self.save()
        self._record(amt, Transaction.TYPE_DEPOSIT, reference, metadata)

    def withdraw(self, amount, reference="", metadata=None):
        """Remove funds from balance (e.g. payout)."""
        amt = Decimal(amount)
        if amt <= 0:
            raise ValidationError("Withdrawal amount must be positive.")
        if amt > self.balance:
            raise ValidationError("Insufficient funds in wallet.")
        self.balance -= amt
        self.save()
        self._record(-amt, Transaction.TYPE_WITHDRAW, reference, metadata)

    def hold_in_escrow(self, amount, reference="", metadata=None):
        """
        Move funds from balance → escrow.
        Used when booking a session/gig but not yet completed.
        """
        amt = Decimal(amount)
        if amt <= 0:
            raise ValidationError("Escrow hold amount must be positive.")
        if amt > self.balance:
            raise ValidationError("Insufficient balance for escrow hold.")
        with transaction.atomic():
            self.balance  -= amt
            self.escrowed += amt
            self.save()
            self._record(-amt, Transaction.TYPE_ESCROW_HOLD, reference, metadata)

    def release_escrow(self, amount, reference="", metadata=None):
        """
        Release escrowed funds back to balance.
        Used on session completion, cancellation, or refund.
        """
        amt = Decimal(amount)
        if amt <= 0:
            raise ValidationError("Escrow release amount must be positive.")
        if amt > self.escrowed:
            raise ValidationError("Insufficient escrowed funds.")
        with transaction.atomic():
            self.escrowed -= amt
            self.balance  += amt
            self.save()
            self._record(amt, Transaction.TYPE_ESCROW_RELEASE, reference, metadata)


class Payment(models.Model):
    """
    One-off payments through external gateways (Stripe, PayPal, etc.)
    that top-up wallets or pay directly for sessions/courses.
    """
    STATUS_PENDING   = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED    = "failed"
    STATUS_REFUNDED  = "refunded"

    STATUS_CHOICES = [
        (STATUS_PENDING,   "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED,    "Failed"),
        (STATUS_REFUNDED,  "Refunded"),
    ]

    user           = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    amount         = models.DecimalField(max_digits=12, decimal_places=2)
    status         = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    method         = models.CharField(
        max_length=50,
        blank=True,
        help_text="Gateway used (e.g. Stripe, PayPal)"
    )
    transaction_id = models.CharField(
        max_length=128,
        blank=True,
        help_text="Provider transaction or order ID"
    )
    metadata       = models.JSONField(
        default=dict,
        blank=True,
        help_text="Extra data (e.g. { 'session_id': 42 })"
    )
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} paid {self.amount:.2f} [{self.status}]"

    def is_successful(self):
        return self.status == self.STATUS_COMPLETED

    def mark_completed(self, txn_id=None):
        """
        Mark a pending payment as completed and store gateway ID.
        """
        self.status = self.STATUS_COMPLETED
        if txn_id:
            self.transaction_id = txn_id
        self.save()

    def mark_failed(self, reason=""):
        """
        Mark a pending payment as failed (e.g. card declined).
        """
        self.status = self.STATUS_FAILED
        if reason:
            self.transaction_id = reason
        self.save()

    def refund(self, reference=""):
        """
        Refund a completed payment:
          1) set status = refunded
          2) optionally auto‐deposit funds back to wallet
        """
        if self.status != self.STATUS_COMPLETED:
            raise ValidationError("Only completed payments can be refunded.")
        self.status = self.STATUS_REFUNDED
        self.save()
        # refund back into wallet:
        self.user.wallet.deposit(self.amount, reference or f"refund-{self.pk}")