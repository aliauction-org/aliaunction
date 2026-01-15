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


@login_required
def bulk_upload(request):
    """
    CSV bulk upload for creating multiple auctions at once.
    Expected CSV format: title,description,starting_price,end_time,category_slug
    """
    import csv
    from io import TextIOWrapper
    from datetime import datetime
    from django.contrib import messages
    from auctions.models import Category
    
    # Sample CSV template for download
    sample_csv = """title,description,starting_price,end_time,category_slug
"Vintage Watch","Beautiful vintage watch from 1960s",5000,2026-02-01 18:00,watches
"Antique Vase","Rare Chinese antique vase",15000,2026-02-03 20:00,antiques
"Art Painting","Original oil painting",25000,2026-02-05 19:00,art"""
    
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            messages.error(request, 'Please upload a CSV file.')
            return render(request, 'dashboard/bulk_upload.html', {'sample_csv': sample_csv})
        
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File must be a CSV file.')
            return render(request, 'dashboard/bulk_upload.html', {'sample_csv': sample_csv})
        
        try:
            # Read CSV file
            decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(decoded_file)
            
            created_count = 0
            errors = []
            
            for row_num, row in enumerate(reader, start=2):  # Start from 2 (1 for header)
                try:
                    # Parse fields
                    title = row.get('title', '').strip()
                    description = row.get('description', '').strip()
                    starting_price = float(row.get('starting_price', 0))
                    end_time_str = row.get('end_time', '').strip()
                    category_slug = row.get('category_slug', '').strip()
                    
                    # Validate required fields
                    if not title:
                        errors.append(f"Row {row_num}: Title is required")
                        continue
                    if not description:
                        errors.append(f"Row {row_num}: Description is required")
                        continue
                    if starting_price <= 0:
                        errors.append(f"Row {row_num}: Starting price must be greater than 0")
                        continue
                    
                    # Parse end time
                    try:
                        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
                        end_time = timezone.make_aware(end_time)
                    except ValueError:
                        errors.append(f"Row {row_num}: Invalid date format. Use YYYY-MM-DD HH:MM")
                        continue
                    
                    # Validate end time is in future
                    if end_time <= timezone.now():
                        errors.append(f"Row {row_num}: End time must be in the future")
                        continue
                    
                    # Get category (optional)
                    category = None
                    if category_slug:
                        try:
                            category = Category.objects.get(slug=category_slug)
                        except Category.DoesNotExist:
                            errors.append(f"Row {row_num}: Category '{category_slug}' not found")
                            continue
                    
                    # Create auction
                    auction = Auction.objects.create(
                        title=title,
                        description=description,
                        starting_price=starting_price,
                        current_price=starting_price,
                        end_time=end_time,
                        owner=request.user,
                        category=category,
                        is_active=True
                    )
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
            
            if created_count > 0:
                messages.success(request, f'Successfully created {created_count} auction(s).')
            
            if errors:
                for error in errors[:10]:  # Show first 10 errors
                    messages.warning(request, error)
                if len(errors) > 10:
                    messages.warning(request, f'... and {len(errors) - 10} more errors.')
            
        except Exception as e:
            messages.error(request, f'Error processing CSV: {str(e)}')
    
    return render(request, 'dashboard/bulk_upload.html', {'sample_csv': sample_csv})

