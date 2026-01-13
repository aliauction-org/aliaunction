from django.db import models
from users.models import User
from auctions.models import Auction

class Report(models.Model):
    REPORT_AUCTION = "AUCTION"
    REPORT_USER = "USER"

    REPORT_TYPE_CHOICES = [
        (REPORT_AUCTION, "Auction"),
        (REPORT_USER, "User"),
    ]

    REASONS = [
        ("FRAUD", "Fraud / Scam"),
        ("FAKE_ITEM", "Fake item"),
        ("WRONG_INFO", "Incorrect information"),
        ("ABUSE", "Abusive behavior"),
        ("OTHER", "Other"),
    ]

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports_made"
    )

    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)

    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    reported_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports_received"
    )

    reason = models.CharField(max_length=20, choices=REASONS)
    description = models.TextField(blank=True)

    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} report by {self.reporter.username}"
