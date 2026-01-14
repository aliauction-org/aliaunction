from django.db import models
from users.models import User
from auctions.models import Auction


class Watchlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlist_items"
    )
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="watchers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Notify me when auction is about to end
    notify_before_end = models.BooleanField(default=False)
    notification_sent = models.BooleanField(default=False)
    
    # Notify on price drops or outbids (future use)
    notify_on_outbid = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "auction")

    def __str__(self):
        return f"{self.user.username} watches {self.auction.title}"

