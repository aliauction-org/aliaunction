from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from auctions.models import Auction
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models import Count
from django.utils import timezone

def live_auctions(request):
    """Live auctions page showing currently active auctions"""
    from django.db.models import Count
    
    auctions = Auction.objects.filter(is_active=True).annotate(
        bid_count=Count('bids')
    ).order_by('-created_at')
    
    # Calculate total bids across all active auctions
    total_bids = auctions.aggregate(total=Count('bids'))['total'] or 0
    
    context = {
        'auctions': auctions,
        'total_bids': total_bids,
        'page_title': 'Live Auctions',
        'page_description': 'Discover and bid on unique items in real-time auctions',
        'now': timezone.now()
    }
    return render(request, 'marketplace/live_auctions.html', context)

def upcoming_items(request):
    """Upcoming items page showing auctions that will start soon"""
    # Get auctions that will end in the next 7 days
    future_date = datetime.now() + timedelta(days=7)
    upcoming_auctions = Auction.objects.filter(
        end_time__gt=datetime.now(),
        end_time__lte=future_date
    ).order_by('end_time')
    
    context = {
        'upcoming_auctions': upcoming_auctions,
        'page_title': 'Upcoming Items',
        'page_description': 'Preview exciting items coming to auction soon',
        'now': timezone.now()
    }
    return render(request, 'marketplace/upcoming_items.html', context)

def sell_with_us(request):
    """Sell with us page with information for sellers"""
    context = {
        'page_title': 'Sell with Us',
        'page_description': 'Start selling your items on AuctionVistas today'
    }
    return render(request, 'marketplace/sell_with_us.html', context)

def categories(request):
    """Categories page showing different auction categories"""
    # Since we don't have categories in the model, we'll use a static list
    categories_data = [
        'Antiques & Collectibles',
        'Art & Paintings', 
        'Jewelry & Watches',
        'Electronics',
        'Home & Garden',
        'Fashion & Accessories',
        'Automotive',
        'Books & Media',
        'Sports & Memorabilia',
        'Wine & Spirits',
        'Gaming & Toys',
        'Health & Beauty'
    ]
    
    context = {
        'categories': categories_data,
        'page_title': 'Categories',
        'page_description': 'Browse auctions by category'
    }
    return render(request, 'marketplace/categories.html', context)

def how_it_works(request):
    """How it works page explaining the auction process"""
    context = {
        'page_title': 'How It Works',
        'page_description': 'Learn how to buy and sell on AuctionVistas'
    }
    return render(request, 'marketplace/how_it_works.html', context)

def help_center(request):
    """Help center page with FAQs and support information"""
    context = {
        'page_title': 'Help Center',
        'page_description': 'Find answers to common questions and get support'
    }
    return render(request, 'marketplace/help_center.html', context)

def buyer_seller_guides(request):
    """Buyer and seller guides page"""
    context = {
        'page_title': 'Buyer & Seller Guides',
        'page_description': 'Comprehensive guides for buyers and sellers'
    }
    return render(request, 'marketplace/buyer_seller_guides.html', context)

def safe_bidding_tips(request):
    """Safe bidding tips page"""
    context = {
        'page_title': 'Safe Bidding Tips',
        'page_description': 'Learn how to bid safely and avoid common pitfalls'
    }
    return render(request, 'marketplace/safe_bidding_tips.html', context)

def contact_support(request):
    """Contact support page"""
    context = {
        'page_title': 'Contact Support',
        'page_description': 'Get in touch with our support team'
    }
    return render(request, 'marketplace/contact_support.html', context)

def terms_privacy(request):
    """Terms and privacy page"""
    context = {
        'page_title': 'Terms & Privacy',
        'page_description': 'Our terms of service and privacy policy'
    }
    return render(request, 'marketplace/terms_privacy.html', context)
