from django.db import models
from auctions.models import Auction

class AuctionCloseMode(models.Model):
    HARD = "HARD"
    SOFT = "SOFT"

    MODE_CHOICES = [
        (HARD, "Hard Close"),
        (SOFT, "Soft Close"),
    ]

    auction = models.OneToOneField(
        Auction,
        on_delete=models.CASCADE,
        related_name="close_mode"
    )
    mode = models.CharField(
        max_length=10,
        choices=MODE_CHOICES,
        default=HARD
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.auction.title} → {self.mode}"
