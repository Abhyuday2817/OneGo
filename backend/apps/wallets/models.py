from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from django.core.exceptions import ValidationError
from apps.transactions.models import Transaction  # Adjusted for app path

class Wallet(models.Model):
    """
    A user's wallet containing:
    - balance: available funds
    - escrowed: funds locked for ongoing services
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet_wallets_app"  # Unique related_name to avoid conflicts
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Available funds"
    )
    escrowed = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Funds held in escrow"
    )

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user.username}: ₹{self.balance:.2f} (Escrowed ₹{self.escrowed:.2f})"

    def _log_transaction(self, amount: Decimal, txn_type: str, reference: str = "", metadata: dict = None):
        """
        Internal helper to log transaction records.
        """
        Transaction.objects.create(
            user=self.user,
            amount=amount,
            txn_type=txn_type,
            reference=reference,
            metadata=metadata or {}
        )

    def deposit(self, amount: Decimal, reference: str = "", metadata: dict = None):
        """
        Add funds to wallet.
        """
        if amount <= 0:
            raise ValidationError("Deposit amount must be positive.")
        with transaction.atomic():
            self.balance = models.F("balance") + amount
            self.save(update_fields=["balance"])
            self._log_transaction(amount, Transaction.TYPE_DEPOSIT, reference, metadata)

    def withdraw(self, amount: Decimal, reference: str = "", metadata: dict = None):
        """
        Withdraw funds from wallet.
        """
        if amount <= 0:
            raise ValidationError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValidationError("Insufficient available balance.")
        with transaction.atomic():
            self.balance = models.F("balance") - amount
            self.save(update_fields=["balance"])
            self._log_transaction(-amount, Transaction.TYPE_WITHDRAW, reference, metadata)

    def hold_in_escrow(self, amount: Decimal, reference: str = "", metadata: dict = None):
        """
        Hold funds in escrow (e.g. during booking).
        """
        if amount <= 0:
            raise ValidationError("Escrow hold amount must be positive.")
        if amount > self.balance:
            raise ValidationError("Insufficient available balance.")
        with transaction.atomic():
            self.balance = models.F("balance") - amount
            self.escrowed = models.F("escrowed") + amount
            self.save(update_fields=["balance", "escrowed"])
            self._log_transaction(-amount, Transaction.TYPE_ESCROW_HOLD, reference, metadata)

    def release_escrow(self, amount: Decimal, reference: str = "", metadata: dict = None):
        """
        Release escrowed funds back to available balance.
        """
        if amount <= 0:
            raise ValidationError("Release amount must be positive.")
        if amount > self.escrowed:
            raise ValidationError("Insufficient escrowed balance.")
        with transaction.atomic():
            self.escrowed = models.F("escrowed") - amount
            self.balance = models.F("balance") + amount
            self.save(update_fields=["escrowed", "balance"])
            self._log_transaction(amount, Transaction.TYPE_ESCROW_RELEASE, reference, metadata)