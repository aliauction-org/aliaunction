from django.db import models
from users.models import User
from auctions.models import Auction
from django.core.exceptions import ValidationError

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

class PaymentProof(models.Model):
    PAYMENT_DIRECTION_CHOICES = [
        ('to_platform', 'To Platform'),
        ('to_user', 'To User'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='payment_proofs')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    payee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    direction = models.CharField(max_length=20, choices=PAYMENT_DIRECTION_CHOICES)
    screenshot = models.ImageField(upload_to='payment_proofs/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')
    comments = models.TextField(blank=True)

class PlatformPaymentDetails(models.Model):
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    account_holder_name = models.CharField(max_length=100)
    upi_id = models.CharField(max_length=50, blank=True)
    qr_code = models.ImageField(upload_to='platform_payment/', blank=True)
    additional_instructions = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Platform Payment Details"

    def save(self, *args, **kwargs):
        if not self.pk and PlatformPaymentDetails.objects.exists():
            raise ValidationError("There can be only one PlatformPaymentDetails instance.")
        super().save(*args, **kwargs)

class UserPaymentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payment_profile')
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    account_holder_name = models.CharField(max_length=100)
    upi_id = models.CharField(max_length=50, blank=True)
    qr_code = models.ImageField(upload_to='user_payment_profiles/', blank=True)
    additional_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
