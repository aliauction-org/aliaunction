from decimal import Decimal
from .models import CommissionRule

def get_active_commission():
    return CommissionRule.objects.filter(is_active=True).last()


def calculate_commission(amount):
    rule = get_active_commission()

    if not rule:
        return Decimal("0.00"), Decimal("0.00")

    seller_fee = (amount * rule.seller_percent) / 100
    buyer_fee = (amount * rule.buyer_percent) / 100

    return seller_fee, buyer_fee
