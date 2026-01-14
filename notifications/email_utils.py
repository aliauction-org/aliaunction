"""
Email notification utilities for auction events.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def send_auction_starting_soon(user, auction):
    """Send notification that an auction is starting soon (24h before)."""
    if not user.email:
        return False
    
    auction_url = f"{settings.DEFAULT_FROM_EMAIL.split('@')[1]}/auctions/{auction.id}/"
    
    send_mail(
        subject=f'🔔 Auction Starting Soon: {auction.title}',
        message=f'''Hello {user.username},

The auction "{auction.title}" is starting in 24 hours!

Don't miss your chance to bid on this item.

View the auction: {auction_url}

Best regards,
AuctionVistas Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return True


def send_auction_ending_soon(user, auction):
    """Send notification that an auction is ending soon (1h before)."""
    if not user.email:
        return False
    
    auction_url = f"{settings.DEFAULT_FROM_EMAIL.split('@')[1]}/auctions/{auction.id}/"
    current_price = auction.current_price
    
    send_mail(
        subject=f'⏰ Auction Ending Soon: {auction.title}',
        message=f'''Hello {user.username},

The auction "{auction.title}" is ending in about 1 hour!

Current highest bid: ₹{current_price:,.2f}

Place your bid now to avoid missing out!

View the auction: {auction_url}

Best regards,
AuctionVistas Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return True


def send_winning_notification(winner, auction, invoice=None):
    """Send notification to auction winner with payment link."""
    if not winner.email:
        return False
    
    base_url = settings.DEFAULT_FROM_EMAIL.split('@')[1]
    auction_url = f"{base_url}/auctions/{auction.id}/"
    
    payment_section = ""
    if invoice:
        payment_url = f"{base_url}/payments/pay/{invoice.id}/"
        payment_section = f'''
Your invoice has been generated.

Total Amount Due: ₹{invoice.total_payable():,.2f}
  - Winning Bid: ₹{invoice.amount:,.2f}
  - Buyer Commission (3%): ₹{invoice.buyer_commission:,.2f}
  - Transport Charges: ₹{invoice.transport_charge:,.2f}

Pay Now: {payment_url}

Payment Options Available:
  • UPI
  • NEFT/IMPS Bank Transfer
  • Cash on Delivery (COD)
'''
    
    send_mail(
        subject=f'🎉 Congratulations! You Won: {auction.title}',
        message=f'''Hello {winner.username},

Great news! You have won the auction for "{auction.title}"!

Winning Bid: ₹{auction.current_price:,.2f}
{payment_section}

View Auction: {auction_url}

Thank you for using AuctionVistas!

Best regards,
AuctionVistas Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[winner.email],
    )
    return True


def send_seller_auction_ended(seller, auction, winner=None):
    """Notify seller that their auction has ended."""
    if not seller.email:
        return False
    
    base_url = settings.DEFAULT_FROM_EMAIL.split('@')[1]
    
    if winner:
        winner_info = f'''
Winner: {winner.username}
Winning Bid: ₹{auction.current_price:,.2f}

The buyer will receive payment instructions. You will be notified once payment is confirmed.
'''
    else:
        winner_info = '''
Unfortunately, there were no bids on this auction.
Consider relisting with a lower starting price.
'''
    
    send_mail(
        subject=f'📢 Your Auction Has Ended: {auction.title}',
        message=f'''Hello {seller.username},

Your auction "{auction.title}" has ended.
{winner_info}

View your auctions dashboard: {base_url}/dashboard/my-auctions/

Best regards,
AuctionVistas Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[seller.email],
    )
    return True
