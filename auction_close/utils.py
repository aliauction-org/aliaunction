from django.utils import timezone

def is_soft_close(auction):
    return hasattr(auction, "close_mode") and auction.close_mode.mode == "SOFT"


def can_finalize_auction(auction, last_bid_time):
    """
    For SOFT close:
    Auction finalizes only when bidding stops
    """
    if not is_soft_close(auction):
        return True

    if not last_bid_time:
        return True

    # If last bid was before end_time → finalize
    return last_bid_time <= auction.end_time
