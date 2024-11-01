from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class PerformanceMetric(models.Model):
    PERFORMANCE_STATUS = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('AVERAGE', 'Average'),
        ('POOR', 'Poor')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performance_metrics')
    credit_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        help_text="Credit score between 0-1000"
    )
    savings_consistency = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of consistent savings"
    )
    repayment_history = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of timely repayments"
    )
    account_activity_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Score based on account transactions"
    )
    membership_duration_months = models.PositiveIntegerField()
    total_shares_value = models.DecimalField(max_digits=12, decimal_places=2)
    performance_status = models.CharField(max_length=20, choices=PERFORMANCE_STATUS)
    loan_eligibility_amount = models.DecimalField(max_digits=12, decimal_places=2)
    last_updated = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Performance - {self.performance_status}"

    def calculate_performance_status(self):
        total_score = (
            (self.credit_score / 10) +
            self.savings_consistency +
            self.repayment_history +
            self.account_activity_score
        ) / 4

        if total_score >= 90:
            self.performance_status = 'EXCELLENT'
        elif total_score >= 75:
            self.performance_status = 'GOOD'
        elif total_score >= 60:
            self.performance_status = 'AVERAGE'
        else:
            self.performance_status = 'POOR'
        self.save()

    def calculate_loan_eligibility(self):
        base_multiplier = {
            'EXCELLENT': 5,
            'GOOD': 3,
            'AVERAGE': 1.5,
            'POOR': 0
        }
        
        multiplier = base_multiplier[self.performance_status]
        total_assets = self.total_shares_value
        
        self.loan_eligibility_amount = total_assets * multiplier
        self.save()
        return self.loan_eligibility_amount

    def update_metrics(self):
        # Update credit score, savings consistency, etc.
        self.calculate_performance_status()
        self.calculate_loan_eligibility()
        self.last_updated = timezone.now()
        self.save()
