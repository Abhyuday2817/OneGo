from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ValidationError


class TransactionQuerySet(models.QuerySet):
    def for_user(self, user):
        """
        Filter transactions for a specific user.
        """
        return self.filter(user=user)

    def of_type(self, txn_type):
        """
        Filter transactions of a specific type.
        """
        return self.filter(txn_type=txn_type)

    def in_period(self, start, end):
        """
        Filter transactions within a specific timestamp range.
        """
        return self.filter(timestamp__gte=start, timestamp__lte=end)


class Transaction(models.Model):
    """
    Immutable ledger entry for wallet and escrow activities.
    Types:
      • deposit        – User adds money to wallet
      • withdraw       – User withdraws funds
      • escrow_hold    – Funds locked for a gig/session
      • escrow_release – Funds released from escrow
    """
    TYPE_DEPOSIT = "deposit"
    TYPE_WITHDRAW = "withdraw"
    TYPE_ESCROW_HOLD = "escrow_hold"
    TYPE_ESCROW_RELEASE = "escrow_release"

    TYPE_CHOICES = [
        (TYPE_DEPOSIT, "Deposit"),
        (TYPE_WITHDRAW, "Withdrawal"),
        (TYPE_ESCROW_HOLD, "Escrow Hold"),
        (TYPE_ESCROW_RELEASE, "Escrow Release"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions_transactions_app"  # Unique related_name to prevent conflicts
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount of the transaction (positive for credit, negative for debit)"
    )
    txn_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(
        max_length=255,
        blank=True,
        help_text="Reference ID (e.g. session#123, refund#456)"
    )
    metadata = models.JSONField(
        blank=True,
        default=dict,
        help_text="Optional data (e.g. {'order_id': 'XYZ'})"
    )

    objects = TransactionQuerySet.as_manager()

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["txn_type"]),
        ]

    def __str__(self):
        sign = "+" if self.is_credit else "-"
        return f"{self.user.username} {self.get_txn_type_display()} {sign}{abs(self.amount):.2f} at {self.timestamp:%Y-%m-%d %H:%M}"

    @property
    def is_credit(self):
        """
        Check if the transaction is a credit (positive amount).
        """
        return self.txn_type in {self.TYPE_DEPOSIT, self.TYPE_ESCROW_RELEASE}

    @property
    def is_debit(self):
        """
        Check if the transaction is a debit (negative amount).
        """
        return self.txn_type in {self.TYPE_WITHDRAW, self.TYPE_ESCROW_HOLD}

    def clean(self):
        """
        Validate transaction data before saving.
        """
        if Decimal(self.amount) <= 0:
            raise ValidationError("Transaction amount must be greater than 0.")

    def save(self, *args, **kwargs):
        """
        Override save method to enforce validation checks.
        """
        self.full_clean()  # Run validations before save
        super().save(*args, **kwargs)