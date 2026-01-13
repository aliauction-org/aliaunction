from django.db.models.signals import pre_save
from django.dispatch import receiver
from auctions.models import Bid
from django.core.exceptions import ValidationError
from .validators import validate_bid

@receiver(pre_save, sender=Bid)
def block_invalid_bid(sender, instance, **kwargs):
    # Only validate new bids
    if instance.pk:
        return

    validate_bid(
        user=instance.user,
        auction=instance.auction,
        amount=instance.amount
    )
