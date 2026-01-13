from django.shortcuts import render
from django.utils import timezone
from auctions.models import Auction
from .forms import AuctionSearchForm
from auction_status.utils import get_auction_status

def discover_auctions(request):
    form = AuctionSearchForm(request.GET or None)
    auctions = Auction.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        live_only = form.cleaned_data.get("live_only")
        ending_soon = form.cleaned_data.get("ending_soon")
        newest = form.cleaned_data.get("newest")

        if q:
            auctions = auctions.filter(title__icontains=q)

        if min_price is not None:
            auctions = auctions.filter(current_price__gte=min_price)

        if max_price is not None:
            auctions = auctions.filter(current_price__lte=max_price)

        if live_only:
            auctions = [a for a in auctions if get_auction_status(a) == "LIVE"]

        if ending_soon:
            auctions = auctions.filter(end_time__gte=timezone.now()).order_by("end_time")

        if newest:
            auctions = auctions.order_by("-created_at")

    return render(
        request,
        "auction_discovery/discover.html",
        {
            "form": form,
            "auctions": auctions
        }
    )
