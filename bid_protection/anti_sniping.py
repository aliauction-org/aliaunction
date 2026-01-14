from django.db import models
from auctions.models import Auction


class AntiSnipingConfig(models.Model):
    """Configuration for anti-sniping feature per auction."""
    auction = models.OneToOneField(
        Auction,
        on_delete=models.CASCADE,
        related_name="anti_sniping"
    )
    threshold_minutes = models.PositiveIntegerField(
        default=5,
        help_text="If a bid is placed within this many minutes of end, extend the auction"
    )
    extension_minutes = models.PositiveIntegerField(
        default=5,
        help_text="Extend the auction by this many minutes"
    )
    is_enabled = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Anti-sniping for {self.auction.title}"
    
    class Meta:
        verbose_name = "Anti-Sniping Configuration"
        verbose_name_plural = "Anti-Sniping Configurations"
