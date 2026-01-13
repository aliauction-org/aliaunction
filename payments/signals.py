from django.db.models.signals import post_save
from django.dispatch import receiver
from auctions.models import Auction
from .models import Invoice
from commission.services import calculation_commission

@receiver(post_save, sender=Auction)
def create_invoice_on_win(sender, instance, **kwargs):
    if not instance.is_active and instance.winner and not hasattr(instance, "invoice"):
        winning_price = instance.current_price

        buyer_fee = winning_price * 0.03
        seller_fee = winning_price * 0.10

        Invoice.objects.create(
            auction=instance,
            buyer=instance.winner,
            seller=instance.seller,
            amount=winning_price,
            buyer_fee=buyer_fee,
            seller_fee=seller_fee,
            transport_charge=0,
        )
