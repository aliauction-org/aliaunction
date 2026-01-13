from .models import Watchlist

def is_watching(user, auction):
    return Watchlist.objects.filter(user=user, auction=auction).exists()


def add_to_watchlist(user, auction):
    Watchlist.objects.get_or_create(user=user, auction=auction)


def remove_from_watchlist(user, auction):
    Watchlist.objects.filter(user=user, auction=auction).delete()
