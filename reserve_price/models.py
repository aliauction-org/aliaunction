from django.db import models
from auctions.models import Auction

class ReservePrice(models.Model):
    auction = models.OneToOneField(
        Auction,
        on_delete=models.CASCADE,
        related_name="reserve"
    )
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    seller_only = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_met(self):
        return self.auction.current_price >= self.amount

    def _str_(self):
        return f"Reserve for {self.auction.title}"
