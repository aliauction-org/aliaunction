from django.utils import timezone
from django.core.exceptions import ValidationError
from auction_status.utils import get_auction_status
from .models import UserStatus

def validate_bid(user, auction, amount):
    # Amount validation
    if amount <= 0:
        raise ValidationError("Bid amount must be greater than zero.")

    # Seller cannot bid
    if auction.owner == user:
        raise ValidationError("You cannot bid on your own auction.")

    # Auction status validation
    status = get_auction_status(auction)
    if status != "LIVE":
        raise ValidationError("Bidding is allowed only on live auctions.")

    # Auction end time
    if timezone.now() >= auction.end_time:
        raise ValidationError("This auction has already ended.")

    # User suspension check
    user_status = UserStatus.objects.filter(user=user, is_suspended=True).first()
    if user_status:
        raise ValidationError("Your account is suspended from bidding.")

    # Bid amount vs current price
    if amount <= auction.current_price:
        raise ValidationError("Bid must be higher than current price.")
