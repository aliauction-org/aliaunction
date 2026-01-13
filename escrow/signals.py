from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Invoice
from .models import Escrow

@receiver(post_save, sender=Invoice)
def create_escrow(sender, instance, created, **kwargs):
    if created:
        Escrow.objects.create(
            auction=instance.auction,
            buyer=instance.buyer,
            seller=instance.seller
        )
