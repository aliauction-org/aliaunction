from django.db.models.signals import post_save
from django.dispatch import receiver
from auctions.models import Auction
from .services import create_seller_deposit

@receiver(post_save, sender=Auction)
def seller_deposit_on_create(sender, instance, created, **kwargs):
    if created:
        create_seller_deposit(instance.seller, instance)
