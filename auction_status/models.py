from django.db import models
from auctions.models import Auction

class AuctionSchedule(models.Model):
    auction = models.OneToOneField(
        Auction,
        on_delete=models.CASCADE,
        related_name="schedule"
    )
    start_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Schedule for {self.auction.title}"
