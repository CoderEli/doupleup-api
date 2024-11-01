from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Share(models.Model):
    SHARE_STATUS = [
        ('AVAILABLE', 'Available'),
        ('SOLD_OUT', 'Sold Out'),
        ('RESERVED', 'Reserved'),
        ('UPCOMING', 'Upcoming')
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    total_shares = models.PositiveIntegerField()
    available_shares = models.PositiveIntegerField()
    minimum_shares = models.PositiveIntegerField(default=1)
    maximum_shares = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=SHARE_STATUS, default='UPCOMING')
    issue_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

    def update_status(self):
        now = timezone.now()
        if self.available_shares == 0:
            self.status = 'SOLD_OUT'
        elif now < self.issue_date:
            self.status = 'UPCOMING'
        elif now >= self.issue_date and self.available_shares > 0:
            self.status = 'AVAILABLE'
        self.save()

    def calculate_total_value(self):
        return self.price_per_share * self.total_shares

class SharePurchase(models.Model):
    PURCHASE_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('FAILED', 'Failed')
    ]

    share = models.ForeignKey(Share, on_delete=models.CASCADE, related_name='purchases')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='share_purchases')
    number_of_shares = models.PositiveIntegerField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=PURCHASE_STATUS, default='PENDING')
    transaction_reference = models.CharField(max_length=100, unique=True)
    certificate_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Purchase - {self.share.name}"

    def calculate_total_amount(self):
        return self.number_of_shares * self.price_per_share

    def complete_purchase(self):
        if self.status == 'PENDING' and self.share.available_shares >= self.number_of_shares:
            self.share.available_shares -= self.number_of_shares
            self.share.save()
            self.share.update_status()
            self.status = 'COMPLETED'
            self.save()
            return True
        return False
