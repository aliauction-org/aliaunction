"""
Management command to send scheduled auction notifications.
Run this via cron job: python manage.py send_scheduled_notifications

Example cron entry (every 5 minutes):
*/5 * * * * cd /path/to/project && python manage.py send_scheduled_notifications
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from auctions.models import Auction
from notifications.email_service import (
    send_auction_starting_soon,
    send_auction_ending_soon,
    send_auction_won_notification,
    send_auction_lost_notification
)


class Command(BaseCommand):
    help = 'Send scheduled auction notifications (starting soon, ending soon, winners)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending',
        )
        parser.add_argument(
            '--minutes-before',
            type=int,
            default=30,
            help='How many minutes before start/end to send notifications (default: 30)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        minutes_before = options['minutes_before']
        now = timezone.now()
        
        self.stdout.write(f'Running notification check at {now}')
        self.stdout.write(f'Looking for auctions starting/ending within {minutes_before} minutes')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No emails will be sent'))
        
        # Find auctions starting soon
        starting_soon_count = self._process_starting_soon(now, minutes_before, dry_run)
        
        # Find auctions ending soon
        ending_soon_count = self._process_ending_soon(now, minutes_before, dry_run)
        
        # Process ended auctions (notify winners)
        ended_count = self._process_ended_auctions(now, dry_run)
        
        self.stdout.write(self.style.SUCCESS(
            f'Done! Starting soon: {starting_soon_count}, Ending soon: {ending_soon_count}, Won/Lost: {ended_count}'
        ))

    def _process_starting_soon(self, now, minutes_before, dry_run):
        """Notify watchers about auctions starting soon."""
        count = 0
        window_start = now
        window_end = now + timedelta(minutes=minutes_before)
        
        # Find auctions with schedule starting in the next X minutes
        from auction_status.models import AuctionSchedule
        try:
            starting_auctions = Auction.objects.filter(
                schedule__start_time__gte=window_start,
                schedule__start_time__lte=window_end
            ).select_related('schedule')
            
            for auction in starting_auctions:
                minutes_until = int((auction.schedule.start_time - now).total_seconds() / 60)
                self.stdout.write(f'  Auction "{auction.title}" starting in {minutes_until} minutes')
                
                if not dry_run:
                    sent = send_auction_starting_soon(auction, minutes_until)
                    count += sent
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'No schedule model or error: {e}'))
        
        return count

    def _process_ending_soon(self, now, minutes_before, dry_run):
        """Notify watchers about auctions ending soon."""
        count = 0
        window_start = now
        window_end = now + timedelta(minutes=minutes_before)
        
        # Find auctions ending in the next X minutes that are still active
        ending_auctions = Auction.objects.filter(
            end_time__gte=window_start,
            end_time__lte=window_end,
            is_active=True
        )
        
        for auction in ending_auctions:
            minutes_until = int((auction.end_time - now).total_seconds() / 60)
            self.stdout.write(f'  Auction "{auction.title}" ending in {minutes_until} minutes')
            
            if not dry_run:
                sent = send_auction_ending_soon(auction, minutes_until)
                count += sent
        
        return count

    def _process_ended_auctions(self, now, dry_run):
        """Notify winners and losing bidders about ended auctions."""
        count = 0
        
        # Find auctions that ended in the last hour and haven't been processed
        window_start = now - timedelta(hours=1)
        window_end = now
        
        ended_auctions = Auction.objects.filter(
            end_time__gte=window_start,
            end_time__lte=window_end,
            is_active=True  # Still marked active but actually ended
        )
        
        for auction in ended_auctions:
            # Get the highest bid
            highest_bid = auction.bids.order_by('-amount', '-timestamp').first()
            
            if highest_bid:
                winner = highest_bid.user
                self.stdout.write(f'  Auction "{auction.title}" won by {winner.username}')
                
                if not dry_run:
                    # Notify winner
                    send_auction_won_notification(winner, auction)
                    count += 1
                    
                    # Notify losing bidders
                    losing_bidders = set(
                        auction.bids.exclude(user=winner).values_list('user', flat=True)
                    )
                    from users.models import User
                    for user_id in losing_bidders:
                        try:
                            user = User.objects.get(id=user_id)
                            send_auction_lost_notification(user, auction, winner.username)
                            count += 1
                        except User.DoesNotExist:
                            pass
                    
                    # Mark auction as inactive
                    auction.is_active = False
                    auction.save(update_fields=['is_active'])
            else:
                self.stdout.write(f'  Auction "{auction.title}" ended with no bids')
                if not dry_run:
                    auction.is_active = False
                    auction.save(update_fields=['is_active'])
        
        return count
