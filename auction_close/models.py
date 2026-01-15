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

    def __str__(self):
        return f"{self.auction.title} → {self.mode}"


class AntiSnipingSettings(models.Model):
    """
    Per-auction anti-sniping configuration.
    If a bid comes in within threshold_minutes of end, extend by extension_minutes.
    """
    auction = models.OneToOneField(
        Auction,
        on_delete=models.CASCADE,
        related_name="anti_sniping"
    )
    is_enabled = models.BooleanField(default=True)
    threshold_minutes = models.PositiveIntegerField(
        default=5,
        help_text="If bid placed within this many minutes of end, trigger extension"
    )
    extension_minutes = models.PositiveIntegerField(
        default=5,
        help_text="Number of minutes to extend auction"
    )
    max_extensions = models.PositiveIntegerField(
        default=10,
        help_text="Maximum number of extensions allowed"
    )
    extensions_used = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Anti-Sniping Settings"
    
    def __str__(self):
        return f"{self.auction.title} - Anti-Sniping ({'ON' if self.is_enabled else 'OFF'})"
    
    def can_extend(self):
        """Check if more extensions are allowed."""
        return self.is_enabled and self.extensions_used < self.max_extensions


class GlobalAuctionSettings(models.Model):
    """
    Global default settings for all auctions (singleton).
    Individual auctions can override these via AntiSnipingSettings.
    """
    default_anti_sniping_enabled = models.BooleanField(default=True)
    default_threshold_minutes = models.PositiveIntegerField(default=5)
    default_extension_minutes = models.PositiveIntegerField(default=5)
    default_max_extensions = models.PositiveIntegerField(default=10)
    
    # Close mode default
    default_close_mode = models.CharField(
        max_length=10,
        choices=AuctionCloseMode.MODE_CHOICES,
        default=AuctionCloseMode.SOFT
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Global Auction Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and GlobalAuctionSettings.objects.exists():
            raise Exception("There can only be one GlobalAuctionSettings instance")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Global Auction Settings"
    
    @classmethod
    def get_settings(cls):
        """Get or create the singleton settings instance."""
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings

