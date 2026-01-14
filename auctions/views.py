from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Auction, Bid
from .forms import AuctionForm, BidForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from notifications.models import Notification
from django.utils import timezone
from django.core.exceptions import ValidationError
from auction_ws.utils import broadcast_auction_update
from bid_protection.validators import validate_bid
from auction_status.utils import get_auction_status
from reserve_price.utils import reserve_status
from reviews.utils import get_reputation
from datetime import timedelta

# Create your views here.


def get_client_ip(request):
    """Extract client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def apply_anti_sniping(auction):
    """
    Check if anti-sniping should extend the auction.
    Returns True if auction was extended.
    """
    if not hasattr(auction, 'anti_sniping'):
        return False
    
    config = auction.anti_sniping
    if not config.is_enabled:
        return False
    
    now = timezone.now()
    time_remaining = auction.end_time - now
    threshold = timedelta(minutes=config.threshold_minutes)
    
    if time_remaining <= threshold:
        # Extend the auction
        extension = timedelta(minutes=config.extension_minutes)
        auction.end_time = auction.end_time + extension
        auction.save(update_fields=['end_time'])
        return True
    
    return False


def auction_list(request):
    auctions = Auction.objects.filter(workflow__status="LIVE").order_by('-created_at')
    
    # Get featured auctions first
    featured = Auction.objects.filter(
        workflow__status="LIVE",
        is_featured=True
    ).order_by('featured_order')
    
    return render(request, 'auctions/auction_list.html', {
        'auctions': auctions,
        'featured_auctions': featured,
        'now': timezone.now()
    })


def send_outbid_email(outbid_user, auction):
    if outbid_user.email:
        send_mail(
            subject=f'You have been outbid on {auction.title}',
            message=f'You have been outbid on the auction "{auction.title}". Visit the auction to place a higher bid.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[outbid_user.email],
        )


def send_auction_won_email(winner, auction):
    if winner.email:
        send_mail(
            subject=f'Congratulations! You won the auction: {auction.title}',
            message=f'You have won the auction "{auction.title}". Please proceed to payment.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[winner.email],
        )


def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    
    # Increment view count
    Auction.objects.filter(id=auction_id).update(view_count=F('view_count') + 1)
    
    bids = auction.bids.order_by('-timestamp')
    reviews = [] 
    gallery_images = auction.images.all()
    has_bid = False
    already_reviewed = False
    is_winner = False
    has_payment_proof = False
    
    if request.user.is_authenticated:
        has_bid = bids.filter(user=request.user).exists()
        # already_reviewed = reviews.filter(user=request.user).exists()
        # Check if user is the winner (highest bidder)
        highest_bid = auction.bids.order_by('-amount', '-timestamp').first()
        if highest_bid and highest_bid.user == request.user:
            is_winner = True
        # Check if user has already uploaded payment proof
        has_payment_proof = auction.payment_proofs.filter(payer=request.user, direction='to_platform').exists()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to bid.')
            return redirect('login')
        
        form = BidForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Use bid_protection validators
            try:
                validate_bid(request.user, auction, amount)
            except ValidationError as e:
                messages.error(request, str(e.message))
                return redirect('auction_detail', auction_id=auction.id)
            
            # Find previous highest bid user
            previous_highest_bid = auction.bids.order_by('-amount', '-timestamp').first()
            
            # Create bid with audit trail
            Bid.objects.create(
                auction=auction,
                user=request.user,
                amount=amount,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
            auction.current_price = amount
            auction.save()
            
            # Apply anti-sniping extension if applicable
            extended = apply_anti_sniping(auction)
            if extended:
                messages.info(request, f'Auction extended by {auction.anti_sniping.extension_minutes} minutes due to late bid.')
            
            # Broadcast via WebSocket
            broadcast_auction_update(
                auction.id,
                {
                    "current_price": str(auction.current_price),
                    "highest_bidder": auction.highest_bid.user.username if auction.highest_bid else None,
                    "end_time": auction.end_time.isoformat() if extended else None,
                }
            )
            
            # Send outbid notification
            if previous_highest_bid and previous_highest_bid.user != request.user:
                send_outbid_email(previous_highest_bid.user, auction)
                send_outbid_notification(previous_highest_bid.user, auction)
            
            messages.success(request, 'Bid placed successfully!')
            return redirect('auction_detail', auction_id=auction.id)
    else:
        form = BidForm()
    
    return render(request, 'auctions/auction_detail.html', {
        'auction': auction, 
        'bids': bids, 
        'form': form, 
        'reviews': reviews, 
        'gallery_images': gallery_images,
        'has_bid': has_bid, 
        'already_reviewed': already_reviewed,
        'is_winner': is_winner,
        'has_payment_proof': has_payment_proof,
        'status': get_auction_status(auction),
        'reserve_status': reserve_status(auction),
        'seller_reputation': get_reputation(auction.owner),
        'countdown_seconds': (auction.end_time - timezone.now()).total_seconds(),
        'now': timezone.now()
    })


def auction_status_api(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    bids = auction.bids.order_by('-timestamp')[:10]
    bid_list = [
        {
            'amount': str(bid.amount),
            'user': bid.user.username,
            'timestamp': bid.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for bid in bids
    ]
    return JsonResponse({
        'current_price': str(auction.current_price),
        'end_time': auction.end_time.isoformat(),
        'bids': bid_list,
    })


@login_required
def create_auction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner = request.user
            auction.current_price = auction.starting_price
            auction.save()
            messages.success(request, 'Auction created successfully!')
            return redirect('auction_detail', auction_id=auction.id)
    else:
        form = AuctionForm()
    return render(request, 'auctions/create_auction.html', {'form': form})


def send_outbid_notification(outbid_user, auction):
    Notification.objects.create(
        user=outbid_user,
        auction=auction,
        message=f'You have been outbid on the auction "{auction.title}".'
    )
