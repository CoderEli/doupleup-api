from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Loan(models.Model):
    LOAN_STATUS = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISBURSED', 'Disbursed'),
        ('COMPLETED', 'Completed'),
        ('DEFAULTED', 'Defaulted')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Annual interest rate
    term_months = models.PositiveIntegerField()  # Loan duration in months
    purpose = models.TextField()
    application_date = models.DateTimeField(default=timezone.now)
    approval_date = models.DateTimeField(null=True, blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='PENDING')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_loans')
    total_payable = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Loan - {self.status}"

    def calculate_total_payable(self):
        principal = self.loan_amount
        rate = self.interest_rate / 100  # Convert percentage to decimal
        time = self.term_months / 12  # Convert months to years
        total = principal * (1 + (rate * time))
        return round(total, 2)

    def calculate_monthly_payment(self):
        if self.total_payable:
            return round(self.total_payable / self.term_months, 2)
        return 0

    def check_eligibility(self):
        # Add your eligibility logic here
        pass

class LoanRepayment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('OVERDUE', 'Overdue')
    ]

    PAYMENT_METHOD = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('ACCOUNT_DEDUCTION', 'Account Deduction')
    ]

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    transaction_reference = models.CharField(max_length=100, unique=True)
    payment_proof = models.FileField(upload_to='loan_repayment_proofs/', null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Repayment for {self.loan.user.username}'s Loan - {self.payment_date}"

    def process_payment(self):
        if self.status == 'PENDING':
            self.status = 'COMPLETED'
            self.loan.amount_paid += self.amount
            self.loan.save()
            
            if self.loan.amount_paid >= self.loan.total_payable:
                self.loan.status = 'COMPLETED'
                self.loan.save()
            
            self.save()
            return True
        return False

    def check_if_overdue(self):
        if self.due_date < timezone.now() and self.status == 'PENDING':
            self.status = 'OVERDUE'
            self.save()
            return True
        return False
