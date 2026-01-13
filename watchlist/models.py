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

    class Meta:
        unique_together = ("user", "auction")

    def __str__(self):
        return f"{self.user.username} watches {self.auction.title}"
