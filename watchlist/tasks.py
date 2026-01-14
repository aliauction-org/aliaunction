"""
Scheduled tasks for watchlist notifications.
Can be run via Django management command or Celery.
"""
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

from .models import Watchlist
from auction_status.utils import get_auction_status


def send_ending_soon_notifications():
    """
    Send notifications to users who have watchlisted auctions
    that are ending within the next hour.
    
    Run this task every 15 minutes via cron or Celery.
    """
    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)
    
    # Find watchlist items where:
    # - notify_before_end is True
    # - notification_sent is False
    # - auction ends within the next hour
    # - auction is still LIVE
    watchlist_items = Watchlist.objects.filter(
        notify_before_end=True,
        notification_sent=False,
        auction__end_time__lte=one_hour_later,
        auction__end_time__gt=now,
    ).select_related('user', 'auction')
    
    notifications_sent = 0
    
    for item in watchlist_items:
        # Verify auction is still live
        if get_auction_status(item.auction) != "LIVE":
            continue
        
        if item.user.email:
            auction = item.auction
            
            send_mail(
                subject=f'⏰ Auction Ending Soon: {auction.title}',
                message=f'''Hello {item.user.username},

You're watching "{auction.title}" and it's ending soon!

Time Remaining: Less than 1 hour
Current Price: ₹{auction.current_price:,.2f}

Don't miss out - place your bid now!

Best regards,
AuctionVistas Team
''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[item.user.email],
            )
            
            # Mark as sent
            item.notification_sent = True
            item.save(update_fields=['notification_sent'])
            notifications_sent += 1
    
    return notifications_sent


def reset_notification_flags():
    """
    Reset notification_sent flags for items where the auction
    has been extended (anti-sniping).
    
    Run this after any auction extension.
    """
    # Find items that were notified but auction end_time is now > 1 hour away
    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)
    
    extended_items = Watchlist.objects.filter(
        notification_sent=True,
        notify_before_end=True,
        auction__end_time__gt=one_hour_later,
    )
    
    count = extended_items.update(notification_sent=False)
    return count
