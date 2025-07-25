from django.db import models
from auctions.models import Auction

# Create your models here.

class AdminCommission(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='commissions')
    commission_amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class AuctionApproval(models.Model):
    auction = models.OneToOneField(Auction, on_delete=models.CASCADE, related_name='approval')
    is_approved = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(auto_now=True)
