"""
Email notification service for AuctionVistas.
Handles sending scheduled notifications for auctions.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from notifications.models import Notification


def send_auction_starting_soon(auction, minutes_until_start=30):
    """
    Send email to users watching an auction that's about to start.
    """
    from watchlist.models import Watchlist
    
    watchers = Watchlist.objects.filter(
        auction=auction,
        notify_before_end=True,
        notification_sent=False
    ).select_related('user')
    
    for watchlist_item in watchers:
        user = watchlist_item.user
        if user.email:
            send_mail(
                subject=f'🔔 Auction Starting Soon: {auction.title}',
                message=f'''Hi {user.username},

The auction "{auction.title}" is starting in {minutes_until_start} minutes!

Don't miss your chance to place your bid.

Starting Price: ₹{auction.starting_price}
Start Time: {auction.schedule.start_time if hasattr(auction, 'schedule') else 'Now'}

View Auction: {settings.DEFAULT_FROM_EMAIL.replace('no-reply@', 'https://').replace('.com', '.com')}/auctions/{auction.id}/

Good luck!
The AuctionVistas Team
''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True
            )
            
            # Create in-app notification
            Notification.objects.create(
                user=user,
                auction=auction,
                message=f'The auction "{auction.title}" is starting soon!'
            )
    
    # Mark notifications as sent
    watchers.update(notification_sent=True)
    
    return watchers.count()


def send_auction_ending_soon(auction, minutes_until_end=30):
    """
    Send email to users watching an auction that's about to end.
    """
    from watchlist.models import Watchlist
    
    watchers = Watchlist.objects.filter(
        auction=auction,
        notify_before_end=True
    ).select_related('user')
    
    # Also notify users who have bid on this auction
    from auctions.models import Bid
    bidders = set(Bid.objects.filter(auction=auction).values_list('user__id', flat=True))
    
    notified_users = set()
    
    for watchlist_item in watchers:
        user = watchlist_item.user
        if user.id not in notified_users and user.email:
            _send_ending_soon_email(user, auction, minutes_until_end)
            notified_users.add(user.id)
    
    # Notify bidders who aren't already watching
    from users.models import User
    for user_id in bidders:
        if user_id not in notified_users:
            try:
                user = User.objects.get(id=user_id)
                if user.email:
                    _send_ending_soon_email(user, auction, minutes_until_end)
                    notified_users.add(user_id)
            except User.DoesNotExist:
                pass
    
    return len(notified_users)


def _send_ending_soon_email(user, auction, minutes_until_end):
    """Helper to send ending soon email."""
    send_mail(
        subject=f'⏰ Auction Ending Soon: {auction.title}',
        message=f'''Hi {user.username},

The auction "{auction.title}" is ending in {minutes_until_end} minutes!

Current Price: ₹{auction.current_price}
End Time: {auction.end_time}

Place your final bid now!

View Auction: /auctions/{auction.id}/

Good luck!
The AuctionVistas Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True
    )
    
    # Create in-app notification
    Notification.objects.create(
        user=user,
        auction=auction,
        message=f'The auction "{auction.title}" is ending soon! Current price: ₹{auction.current_price}'
    )


def send_auction_won_notification(winner, auction):
    """
    Send winning notification email and create invoice prompt.
    """
    if winner.email:
        send_mail(
            subject=f'🎉 Congratulations! You Won: {auction.title}',
            message=f'''Hi {winner.username},

Congratulations! You have won the auction for "{auction.title}"!

Winning Bid: ₹{auction.current_price}
Seller: {auction.owner.username}

Please proceed to checkout to complete your purchase.

Checkout: /payments/checkout/{auction.id}/

Thank you for using AuctionVistas!
The AuctionVistas Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[winner.email],
            fail_silently=True
        )
    
    # Create in-app notification
    Notification.objects.create(
        user=winner,
        auction=auction,
        message=f'🎉 Congratulations! You won the auction "{auction.title}"! Click to proceed to checkout.'
    )


def send_auction_lost_notification(user, auction, winner_username):
    """
    Send notification to losing bidders.
    """
    if user.email:
        send_mail(
            subject=f'Auction Ended: {auction.title}',
            message=f'''Hi {user.username},

The auction for "{auction.title}" has ended.

Unfortunately, you were outbid. The winning bid was ₹{auction.current_price} by {winner_username}.

Don't worry - there are more great auctions waiting for you!

Browse Auctions: /auctions/

Thank you for participating!
The AuctionVistas Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )
