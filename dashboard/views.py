"""
Dashboard views for sellers and buyers.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum

from auctions.models import Auction
from auction_status.utils import get_auction_status
from watchlist.models import Watchlist


@login_required
def my_auctions(request):
    """
    Seller dashboard showing all their auctions with stats.
    """
    user = request.user
    
    # Get all auctions by this user
    auctions = Auction.objects.filter(owner=user).order_by('-created_at')
    
    # Separate by status
    live_auctions = []
    ended_auctions = []
    draft_auctions = []
    
    for auction in auctions:
        status = get_auction_status(auction)
        auction.current_status = status
        
        # Add stats
        auction.watcher_count = Watchlist.objects.filter(auction=auction).count()
        auction.bid_count = auction.bids.count()
        
        if hasattr(auction, 'workflow'):
            if auction.workflow.status == 'DRAFT':
                draft_auctions.append(auction)
                continue
            elif auction.workflow.status == 'PENDING':
                draft_auctions.append(auction)
                continue
        
        if status == 'LIVE':
            live_auctions.append(auction)
        else:
            ended_auctions.append(auction)
    
    # Calculate totals
    total_views = sum(a.view_count for a in auctions)
    total_bids = sum(a.bid_count for a in auctions)
    total_watchers = sum(a.watcher_count for a in auctions)
    
    return render(request, 'dashboard/my_auctions.html', {
        'live_auctions': live_auctions,
        'ended_auctions': ended_auctions,
        'draft_auctions': draft_auctions,
        'total_auctions': len(auctions),
        'total_views': total_views,
        'total_bids': total_bids,
        'total_watchers': total_watchers,
    })


@login_required
def my_bids(request):
    """
    Buyer dashboard showing all their bids.
    """
    user = request.user
    
    # Get all auctions the user has bid on
    from auctions.models import Bid
    user_bids = Bid.objects.filter(user=user).select_related('auction').order_by('-timestamp')
    
    # Group bids by auction
    auctions_bid_on = {}
    for bid in user_bids:
        if bid.auction.id not in auctions_bid_on:
            auction = bid.auction
            auction.current_status = get_auction_status(auction)
            auction.user_highest_bid = bid.amount
            auction.is_winning = (auction.highest_bid and auction.highest_bid.user == user)
            auctions_bid_on[auction.id] = auction
        else:
            # Update if this is a higher bid
            if bid.amount > auctions_bid_on[bid.auction.id].user_highest_bid:
                auctions_bid_on[bid.auction.id].user_highest_bid = bid.amount
    
    # Separate by status
    active_bids = []
    won_auctions = []
    lost_auctions = []
    
    for auction in auctions_bid_on.values():
        if auction.current_status == 'LIVE':
            active_bids.append(auction)
        elif auction.is_winning:
            won_auctions.append(auction)
        else:
            lost_auctions.append(auction)
    
    return render(request, 'dashboard/my_bids.html', {
        'active_bids': active_bids,
        'won_auctions': won_auctions,
        'lost_auctions': lost_auctions,
        'total_bids': len(user_bids),
    })


@login_required
def dashboard_home(request):
    """
    Main dashboard home page with overview.
    """
    user = request.user
    
    # User's auction stats
    my_auction_count = Auction.objects.filter(owner=user).count()
    from auctions.models import Bid
    my_bid_count = Bid.objects.filter(user=user).count()
    watchlist_count = Watchlist.objects.filter(user=user).count()
    
    # Recent activity
    recent_bids = Bid.objects.filter(user=user).select_related('auction').order_by('-timestamp')[:5]
    
    return render(request, 'dashboard/home.html', {
        'my_auction_count': my_auction_count,
        'my_bid_count': my_bid_count,
        'watchlist_count': watchlist_count,
        'recent_bids': recent_bids,
    })
