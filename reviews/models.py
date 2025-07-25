from django.db import models
from users.models import User
from auctions.models import Auction

# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
