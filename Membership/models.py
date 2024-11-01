from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MembershipFee(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled')
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('CARD', 'Credit/Debit Card')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES)
    transaction_reference = models.CharField(max_length=100, unique=True)
    payment_proof = models.FileField(upload_to='payment_proofs/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')
    verification_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Membership Fee - {self.payment_status}"

    def is_full_member(self):
        return self.payment_status == 'PAID' and self.is_verified

    def mark_as_verified(self, verified_by_user):
        self.is_verified = True
        self.verified_by = verified_by_user
        self.verification_date = timezone.now()
        self.save()

    def check_payment_status(self):
        if self.due_date < timezone.now() and self.payment_status == 'PENDING':
            self.payment_status = 'OVERDUE'
            self.save()
        return self.payment_status
