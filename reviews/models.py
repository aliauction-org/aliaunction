from django.db import models
from users.models import User
from escrow.models import Escrow

class Rating(models.Model):
    ROLE_CHOICES = [
        ("BUYER", "Buyer"),
        ("SELLER", "Seller"),
    ]

    escrow = models.OneToOneField(
        Escrow,
        on_delete=models.CASCADE,
        related_name="rating"
    )

    given_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings_given"
    )

    given_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings_received"
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    stars = models.PositiveSmallIntegerField()
    review = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("escrow", "role")

    def __str__(self):
        return f"{self.stars}★ - {self.given_to}"
