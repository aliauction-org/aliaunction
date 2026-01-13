from django.utils import timezone

def get_auction_status(auction):
    now = timezone.now()

    # If schedule exists → check start time
    if hasattr(auction, "schedule"):
        if now < auction.schedule.start_time:
            return "UPCOMING"

    if auction.is_active and now < auction.end_time:
        return "LIVE"

    return "ENDED"


def get_countdown_seconds(auction):
    now = timezone.now()

    if hasattr(auction, "schedule") and now < auction.schedule.start_time:
        return int((auction.schedule.start_time - now).total_seconds())

    if now < auction.end_time:
        return int((auction.end_time - now).total_seconds())

    return 0
