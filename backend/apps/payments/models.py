from decimal import Decimal
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.sessions.models import Session

class Transaction(models.Model):
    TYPE_DEPOSIT        = "deposit"
    TYPE_WITHDRAW       = "withdraw"
    TYPE_ESCROW_HOLD    = "escrow_hold"
    TYPE_ESCROW_RELEASE = "escrow_release"
    TYPE_DEDUCTION      = "deduction"
    TYPE_PAYOUT         = "payout"

    TYPE_CHOICES = [
        (TYPE_DEPOSIT,        "Deposit"),
        (TYPE_WITHDRAW,       "Withdraw"),
        (TYPE_ESCROW_HOLD,    "Escrow Hold"),
        (TYPE_ESCROW_RELEASE, "Escrow Release"),
        (TYPE_DEDUCTION,      "Deduction"),
        (TYPE_PAYOUT,         "Mentor Payout"),
    ]

    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    session   = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    amount    = models.DecimalField(max_digits=12, decimal_places=2)
    txn_type  = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reference = models.CharField(max_length=255, blank=True)
    metadata  = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [models.Index(fields=["user", "txn_type", "timestamp"])]

    def __str__(self):
        sign = "+" if self.txn_type in (self.TYPE_DEPOSIT, self.TYPE_ESCROW_RELEASE) else "-"
        return f"{self.user.username} {self.txn_type} {sign}{abs(self.amount):.2f}"

class Wallet(models.Model):
    user     = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    balance  = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    escrowed = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user.username}: balance={self.balance:.2f} (escrowed={self.escrowed:.2f})"

    def _record(self, amount, txn_type, reference="", metadata=None):
        Transaction.objects.create(
            user=self.user,
            amount=amount,
            txn_type=txn_type,
            reference=reference,
            metadata=metadata or {}
        )

    def deposit(self, amount, reference="", metadata=None):
        amt = Decimal(amount)
        if amt <= 0:
            raise ValidationError("Deposit amount must be positive.")
        self.balance += amt
        self.save()
        self._record(amt, Transaction.TYPE_DEPOSIT, reference, metadata)

    def withdraw(self, amount, reference="", metadata=None):
        amt = Decimal(amount)
        if amt <= 0:
            raise ValidationError("Withdrawal amount must be positive.")
        if amt > self.balance:
            raise ValidationError("Insufficient funds in wallet.")
        self.balance -= amt
        self.save()
        self._record(-amt, Transaction.TYPE_WITHDRAW, reference, metadata)

    def hold_in_escrow(self, amount, reference="", metadata=None):
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

class SessionPayment(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_payments')
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_earnings')
    rate_per_minute = models.DecimalField(max_digits=6, decimal_places=2)
    duration_minutes = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        self.total_amount = self.rate_per_minute * self.duration_minutes
        return self.total_amount

    def process_payment(self):
        self.calculate_total()

        if not self.student.wallet.withdraw(self.total_amount):
            raise ValidationError("Insufficient balance in student wallet")

        self.mentor.wallet.deposit(self.total_amount)

        self.is_paid = True
        self.save()

        Transaction.objects.create(
            user=self.student,
            session=self.session,
            amount=self.total_amount,
            txn_type=Transaction.TYPE_DEDUCTION,
            reference=f"Session#{self.session.id}"
        )

        Transaction.objects.create(
            user=self.mentor,
            session=self.session,
            amount=self.total_amount,
            txn_type=Transaction.TYPE_PAYOUT,
            reference=f"Session#{self.session.id}"
        )

class Payment(models.Model):
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

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    amount         = models.DecimalField(max_digits=12, decimal_places=2)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    method         = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=128, blank=True)
    metadata       = models.JSONField(default=dict, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} paid {self.amount:.2f} [{self.status}]"

    def is_successful(self):
        return self.status == self.STATUS_COMPLETED

    def mark_completed(self, txn_id=None):
        self.status = self.STATUS_COMPLETED
        if txn_id:
            self.transaction_id = txn_id
        self.save()

    def mark_failed(self, reason=""):
        self.status = self.STATUS_FAILED
        if reason:
            self.transaction_id = reason
        self.save()

    def refund(self, reference=""):
        if self.status != self.STATUS_COMPLETED:
            raise ValidationError("Only completed payments can be refunded.")
        self.status = self.STATUS_REFUNDED
        self.save()
        self.user.wallet.deposit(self.amount, reference or f"refund-{self.pk}")
