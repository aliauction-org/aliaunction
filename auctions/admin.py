from django.contrib import admin
from .models import Auction, Bid, ProxyBid
from notifications.models import Notification
from django.core.mail import send_mail
from django.conf import settings

def approve_auctions(modeladmin, request, queryset):
    queryset.update(is_active=True)
approve_auctions.short_description = "Approve selected auctions"

def block_auctions(modeladmin, request, queryset):
    queryset.update(is_active=False)
block_auctions.short_description = "Block selected auctions"

def end_auctions(modeladmin, request, queryset):
    for auction in queryset:
        if auction.is_active:
            auction.is_active = False
            auction.save()
            # Notify winner
            highest_bid = auction.bids.order_by('-amount', '-timestamp').first()
            if highest_bid:
                Notification.objects.create(
                    user=highest_bid.user,
                    auction=auction,
                    message=f'Congratulations! You have won the auction "{auction.title}".'
                )
                send_mail(
                    subject=f'You won the auction: {auction.title}',
                    message=f'You have won the auction "{auction.title}". Please proceed to payment.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[highest_bid.user.email],
                )
            # Notify seller
            Notification.objects.create(
                user=auction.owner,
                auction=auction,
                message=f'Your auction "{auction.title}" has ended.'
            )
end_auctions.short_description = "End selected auctions and notify winner/seller"

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'current_price', 'is_active', 'end_time')
    list_filter = ('is_active', 'end_time')
    search_fields = ('title', 'owner__username')
    actions = [approve_auctions, block_auctions, end_auctions]

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'amount', 'timestamp')
    list_filter = ('auction', 'user')
    search_fields = ('auction__title', 'user__username')

@admin.register(ProxyBid)
class ProxyBidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'max_bid', 'created_at')
    list_filter = ('auction', 'user')
    search_fields = ('auction__title', 'user__username')
