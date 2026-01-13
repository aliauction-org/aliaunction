from .models import Deposit
from .rules import get_buyer_deposit

def has_active_buyer_deposit(user):
    return Deposit.objects.filter(
        user=user,
        deposit_type="BUYER",
        status="LOCKED"
    ).exists()


def create_buyer_deposit(user, auction):
    return Deposit.objects.create(
        user=user,
        auction=auction,
        deposit_type="BUYER",
        amount=get_buyer_deposit()
    )
