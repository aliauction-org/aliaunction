from django.db.models.signals import post_save
from django.dispatch import receiver
from auctions.models import Auction
from .utils import reserve_status

@receiver(post_save, sender=Auction)
def invalidate_winner_if_reserve_not_met(sender, instance, **kwargs):
    if not instance.is_active:
        status = reserve_status(instance)
        if status == "NOT_MET":
            # Auction ended without valid winner
            # No winner payment should proceed
            instance.winner_invalid = True
