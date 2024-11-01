from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class MembershipStatus(models.Model):
    MEMBERSHIP_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    status = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='PENDING')
    membership_start_date = models.DateTimeField(default=timezone.now)
    membership_end_date = models.DateTimeField()
    last_payment_date = models.DateTimeField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Membership - {self.status}"

    def check_membership_status(self):
        now = timezone.now()
        if now > self.membership_end_date:
            self.status = 'EXPIRED'
            self.is_active = False
            self.save()
        return self.is_active
