from django.db import models
from users.models import User
from auctions.models import Auction

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
