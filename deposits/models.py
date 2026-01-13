from django.db import models
from users.models import User
from auctions.models import Auction

class Deposit(models.Model):
    DEPOSIT_TYPE = [
        ("BUYER", "Buyer Deposit"),
        ("SELLER", "Seller Deposit"),
    ]

    STATUS = [
        ("LOCKED", "Locked"),
        ("REFUNDED", "Refunded"),
        ("FORFEITED", "Forfeited"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    deposit_type = models.CharField(max_length=10, choices=DEPOSIT_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="LOCKED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.deposit_type} | {self.user.username} | {self.amount}"
