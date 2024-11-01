from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Account - {self.account_number}"

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    def get_balance(self):
        return self.balance

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('MEMBERSHIP_FEE', 'Membership Fee'),
        ('SHARE_PURCHASE', 'Share Purchase'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer')
    ]

    TRANSACTION_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled')
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS, default='PENDING')
    reference_number = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    transaction_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account.user.username}'s {self.transaction_type} - {self.reference_number}"

    def complete_transaction(self):
        if self.status == 'PENDING':
            if self.transaction_type == 'DEPOSIT':
                self.account.deposit(self.amount)
            elif self.transaction_type in ['MEMBERSHIP_FEE', 'SHARE_PURCHASE', 'WITHDRAWAL']:
                if self.account.withdraw(self.amount):
                    self.status = 'COMPLETED'
                else:
                    self.status = 'FAILED'
            self.save()
        return self.status
