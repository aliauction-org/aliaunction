from django.db import models
from users.models import User
from auctions.models import Auction

class Dispute(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("REVIEW", "Under Review"),
        ("RESOLVED", "Resolved"),
        ("REJECTED", "Rejected"),
    ]

    ISSUE_CHOICES = [
        ("NOT_RECEIVED", "Item not received"),
        ("DAMAGED", "Item damaged"),
        ("NOT_AS_DESCRIBED", "Not as described"),
        ("PAYMENT", "Payment issue"),
        ("OTHER", "Other"),
    ]

    raised_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="disputes_raised"
    )

    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="disputes"
    )

    issue_type = models.CharField(max_length=30, choices=ISSUE_CHOICES)
    description = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute #{self.id} - {self.status}"
