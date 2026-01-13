from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from auctions.models import Auction
from .services import add_to_watchlist, remove_from_watchlist
from .models import Watchlist

@login_required
def toggle_watchlist(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    if Watchlist.objects.filter(user=request.user, auction=auction).exists():
        remove_from_watchlist(request.user, auction)
    else:
        add_to_watchlist(request.user, auction)

    return redirect("auction_detail", auction_id=auction.id)


@login_required
def my_watchlist(request):
    items = Watchlist.objects.filter(user=request.user).select_related("auction")
    return render(request, "watchlist/my_watchlist.html", {"items": items})
