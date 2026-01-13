from decimal import Decimal

BUYER_DEPOSIT_AMOUNT = Decimal("1000.00")
SELLER_DEPOSIT_AMOUNT = Decimal("500.00")

def get_buyer_deposit():
    return BUYER_DEPOSIT_AMOUNT

def get_seller_deposit():
    return SELLER_DEPOSIT_AMOUNT
