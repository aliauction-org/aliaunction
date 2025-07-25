from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Auction, Bid
from .forms import AuctionForm, BidForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from notifications.models import Notification


# Create your views here.


def auction_list(request):
    auctions = Auction.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'auctions/auction_list.html', {'auctions': auctions})


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
    bids = auction.bids.order_by('-timestamp')
    reviews = auction.reviews.select_related('user')
    has_bid = False
    already_reviewed = False
    is_winner = False
    has_payment_proof = False
    
    if request.user.is_authenticated:
        has_bid = bids.filter(user=request.user).exists()
        already_reviewed = reviews.filter(user=request.user).exists()
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
            if amount > auction.current_price:
                # Find previous highest bid user
                previous_highest_bid = auction.bids.order_by('-amount', '-timestamp').first()
                Bid.objects.create(auction=auction, user=request.user, amount=amount)
                auction.current_price = amount
                auction.save()
                # Send outbid email
                if previous_highest_bid and previous_highest_bid.user != request.user:
                    send_outbid_email(previous_highest_bid.user, auction)
                    send_outbid_notification(previous_highest_bid.user, auction)
                messages.success(request, 'Bid placed successfully!')
                return redirect('auction_detail', auction_id=auction.id)
            else:
                messages.error(request, 'Bid must be higher than current price.')
    else:
        form = BidForm()
    return render(request, 'auctions/auction_detail.html', {
        'auction': auction, 
        'bids': bids, 
        'form': form, 
        'reviews': reviews, 
        'has_bid': has_bid, 
        'already_reviewed': already_reviewed,
        'is_winner': is_winner,
        'has_payment_proof': has_payment_proof
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
