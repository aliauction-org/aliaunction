from django.db.models.signals import post_save
from django.dispatch import receiver
from auctions.models import Auction
from .utils import can_finalize_auction

@receiver(post_save, sender=Auction)
def handle_soft_close(sender, instance, **kwargs):
    if instance.is_active:
        return

    bids = instance.bids.order_by("-timestamp")
    last_bid = bids.first()

    if hasattr(instance, "close_mode") and instance.close_mode.mode == "SOFT":
        if last_bid and last_bid.timestamp > instance.end_time:
            # Auction should remain logically open until bidding stops
            instance.is_active = True
            instance.save(update_fields=["is_active"])
