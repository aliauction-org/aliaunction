from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, Rating
from .forms import ReviewRatingForm
from auctions.models import Auction, Bid
from django.db import models as forms

# Create your views here.

@login_required
def submit_review(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    user = request.user
    has_bid = Bid.objects.filter(auction=auction, user=user).exists()
    already_reviewed = Review.objects.filter(auction=auction, user=user).exists()
    if not has_bid:
        messages.error(request, 'You must bid on this auction to leave a review.')
        return redirect('auction_detail', auction_id=auction.id)
    if already_reviewed:
        messages.error(request, 'You have already reviewed this auction.')
        return redirect('auction_detail', auction_id=auction.id)
    if request.method == 'POST':
        form = ReviewRatingForm(request.POST)
        if form.is_valid():
            review = Review.objects.create(
                user=user,
                auction=auction,
                content=form.cleaned_data['content']
            )
            Rating.objects.create(
                user=user,
                auction=auction,
                score=form.cleaned_data['score']
            )
            messages.success(request, 'Thank you for your review!')
            return redirect('auction_detail', auction_id=auction.id)
    else:
        form = ReviewRatingForm()
    return render(request, 'reviews/submit_review.html', {'form': form, 'auction': auction})

def auction_reviews(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    reviews = Review.objects.filter(auction=auction).select_related('user')
    ratings = Rating.objects.filter(auction=auction)
    avg_rating = ratings.aggregate(avg=forms.models.Avg('score'))['avg'] if ratings.exists() else None
    return render(request, 'reviews/auction_reviews.html', {'auction': auction, 'reviews': reviews, 'avg_rating': avg_rating})
