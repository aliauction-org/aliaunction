from .utils import get_auction_status, get_countdown_seconds

def auction_status_context(request):
    return {
        "get_auction_status": get_auction_status,
        "get_countdown_seconds": get_countdown_seconds,
    }
