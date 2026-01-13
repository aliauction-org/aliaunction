from django.db import models
from auctions.models import Auction
from users.models import User

class Escrow(models.Model):
    STATUS_CHOICES = [
        ("PENDING_PAYMENT", "Pending Payment"),
        ("PAID", "Paid"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("COMPLETED", "Completed"),
    ]

    auction = models.OneToOneField(
        Auction,
        on_delete=models.CASCADE,
        related_name="escrow"
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="escrows_as_buyer"
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="escrows_as_seller"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING_PAYMENT"
    )

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Escrow {self.auction.title} - {self.status}"
