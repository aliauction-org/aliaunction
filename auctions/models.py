from django.db import models
from users.models import User

# Create your models here.

class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=20, decimal_places=2)
    current_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class ProxyBid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='proxy_bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proxy_bids')
    max_bid = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
