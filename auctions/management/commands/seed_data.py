"""
Management command to seed the database with test data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with test users, categories, auctions, bids, etc.'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database with test data...\n')
        
        # Import models here to avoid circular imports
        from auctions.models import Auction, Bid, Category, AuctionImage
        from watchlist.models import Watchlist
        
        # Try importing optional models
        try:
            from workflows.models import Workflow
            has_workflow = True
        except ImportError:
            has_workflow = False
        
        try:
            from escrow.models import Escrow
            has_escrow = True
        except ImportError:
            has_escrow = False

        try:
            from reviews.models import Rating
            has_ratings = True
        except ImportError:
            has_ratings = False

        # =====================
        # 1. CREATE USERS
        # =====================
        self.stdout.write('👤 Creating users...')
        
        # Admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@auctionvistas.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Created admin (password: admin123)'))
        else:
            self.stdout.write('  → admin already exists')

        # Seller users
        sellers = []
        seller_data = [
            ('seller1', 'seller1@example.com', 'Rahul Sharma'),
            ('seller2', 'seller2@example.com', 'Priya Patel'),
            ('seller3', 'seller3@example.com', 'Amit Kumar'),
        ]
        for username, email, name in seller_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': name.split()[0], 'last_name': name.split()[-1]}
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created {username}'))
            sellers.append(user)

        # Buyer users
        buyers = []
        buyer_data = [
            ('buyer1', 'buyer1@example.com', 'Sneha Gupta'),
            ('buyer2', 'buyer2@example.com', 'Vikram Singh'),
            ('buyer3', 'buyer3@example.com', 'Anita Desai'),
            ('buyer4', 'buyer4@example.com', 'Rajesh Khanna'),
        ]
        for username, email, name in buyer_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': name.split()[0], 'last_name': name.split()[-1]}
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created {username}'))
            buyers.append(user)

        # =====================
        # 2. CREATE CATEGORIES
        # =====================
        self.stdout.write('\n📁 Creating categories...')
        
        category_data = [
            ('Electronics', 'electronics', 1),
            ('Collectibles', 'collectibles', 2),
            ('Art & Antiques', 'art-antiques', 3),
            ('Vehicles', 'vehicles', 4),
            ('Fashion & Accessories', 'fashion', 5),
            ('Home & Garden', 'home-garden', 6),
            ('Sports & Outdoors', 'sports', 7),
            ('Jewelry & Watches', 'jewelry', 8),
        ]
        
        categories = {}
        for name, slug, order in category_data:
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'order': order, 'is_active': True}
            )
            categories[slug] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {name}'))

        # =====================
        # 3. CREATE AUCTIONS
        # =====================
        self.stdout.write('\n🏷️ Creating auctions...')
        
        now = timezone.now()
        
        auction_data = [
            # Active auctions (ending in future)
            {
                'title': 'iPhone 15 Pro Max 256GB',
                'description': 'Brand new, sealed iPhone 15 Pro Max. Natural Titanium color. Full warranty.',
                'starting_price': Decimal('85000'),
                'current_price': Decimal('92000'),
                'category': 'electronics',
                'owner': sellers[0],
                'end_time': now + timedelta(days=3),
                'is_featured': True,
                'featured_order': 1,
            },
            {
                'title': 'Vintage Rolex Submariner 1968',
                'description': 'Rare vintage Rolex Submariner from 1968. Original parts, serviced recently.',
                'starting_price': Decimal('450000'),
                'current_price': Decimal('520000'),
                'category': 'jewelry',
                'owner': sellers[1],
                'end_time': now + timedelta(days=5),
                'is_featured': True,
                'featured_order': 2,
            },
            {
                'title': 'Royal Enfield Classic 350 - 2020',
                'description': 'Well maintained Royal Enfield Classic 350. Only 15000km driven. All papers clear.',
                'starting_price': Decimal('120000'),
                'current_price': Decimal('135000'),
                'category': 'vehicles',
                'owner': sellers[2],
                'end_time': now + timedelta(days=7),
                'is_featured': False,
            },
            {
                'title': 'Sony PlayStation 5 with 2 Controllers',
                'description': 'PS5 Disc Edition with 2 DualSense controllers. Includes 3 games.',
                'starting_price': Decimal('45000'),
                'current_price': Decimal('48500'),
                'category': 'electronics',
                'owner': sellers[0],
                'end_time': now + timedelta(days=2),
                'is_featured': False,
            },
            {
                'title': 'Antique Tanjore Painting - Krishna',
                'description': '19th century Tanjore painting depicting Lord Krishna. Gold leaf work, excellent condition.',
                'starting_price': Decimal('75000'),
                'current_price': Decimal('82000'),
                'category': 'art-antiques',
                'owner': sellers[1],
                'end_time': now + timedelta(days=10),
                'is_featured': True,
                'featured_order': 3,
            },
            {
                'title': 'Cricket Bat signed by Sachin Tendulkar',
                'description': 'Authentic MRF bat signed by the legend himself. Comes with certificate of authenticity.',
                'starting_price': Decimal('25000'),
                'current_price': Decimal('38000'),
                'category': 'sports',
                'owner': sellers[2],
                'end_time': now + timedelta(days=4),
                'is_featured': False,
            },
            {
                'title': 'Rare 1947 Indian Independence Coin Set',
                'description': 'Complete set of 1947 commemorative coins. Uncirculated condition.',
                'starting_price': Decimal('15000'),
                'current_price': Decimal('15000'),
                'category': 'collectibles',
                'owner': sellers[0],
                'end_time': now + timedelta(days=6),
                'is_featured': False,
            },
            {
                'title': 'Designer Banarasi Silk Saree',
                'description': 'Handwoven pure silk Banarasi saree with intricate zari work. Wedding collection.',
                'starting_price': Decimal('35000'),
                'current_price': Decimal('42000'),
                'category': 'fashion',
                'owner': sellers[1],
                'end_time': now + timedelta(days=3),
                'is_featured': False,
            },
            # Ended auctions (for testing winner flows)
            {
                'title': 'MacBook Pro M3 14-inch',
                'description': 'Barely used MacBook Pro M3. 16GB RAM, 512GB SSD. Still under AppleCare+.',
                'starting_price': Decimal('150000'),
                'current_price': Decimal('168000'),
                'category': 'electronics',
                'owner': sellers[2],
                'end_time': now - timedelta(days=1),
                'is_featured': False,
            },
            {
                'title': 'Vintage Vespa Scooter 1975',
                'description': 'Fully restored 1975 Vespa. Running condition, registered.',
                'starting_price': Decimal('95000'),
                'current_price': Decimal('125000'),
                'category': 'vehicles',
                'owner': sellers[0],
                'end_time': now - timedelta(days=3),
                'is_featured': False,
            },
        ]

        auctions = []
        for data in auction_data:
            cat_slug = data.pop('category')
            auction, created = Auction.objects.get_or_create(
                title=data['title'],
                defaults={
                    **data,
                    'category': categories.get(cat_slug),
                    'is_active': data['end_time'] > now,
                }
            )
            auctions.append(auction)
            
            # Create workflow if model exists
            if has_workflow and created:
                try:
                    Workflow.objects.get_or_create(
                        auction=auction,
                        defaults={'status': 'LIVE' if auction.is_active else 'ENDED'}
                    )
                except Exception:
                    pass
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {auction.title[:40]}...'))

        # =====================
        # 4. CREATE BIDS
        # =====================
        self.stdout.write('\n💰 Creating bids...')
        
        bid_count = 0
        for auction in auctions:
            # Skip auctions at starting price
            if auction.current_price == auction.starting_price:
                continue
            
            # Create bid history
            price = auction.starting_price
            increment = (auction.current_price - auction.starting_price) / 3
            
            for i, buyer in enumerate(random.sample(buyers, min(3, len(buyers)))):
                if buyer == auction.owner:
                    continue
                price += increment
                if price > auction.current_price:
                    price = auction.current_price
                    
                bid, created = Bid.objects.get_or_create(
                    auction=auction,
                    user=buyer,
                    amount=price,
                    defaults={
                        'ip_address': f'192.168.1.{random.randint(1, 255)}',
                        'user_agent': 'Mozilla/5.0 (Test Browser)'
                    }
                )
                if created:
                    bid_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {bid_count} bids'))

        # =====================
        # 5. CREATE WATCHLIST ENTRIES
        # =====================
        self.stdout.write('\n👁️ Creating watchlist entries...')
        
        watchlist_count = 0
        for buyer in buyers:
            # Each buyer watches 2-3 random auctions
            watched = random.sample(auctions[:8], min(3, len(auctions)))
            for auction in watched:
                if auction.owner != buyer:
                    wl, created = Watchlist.objects.get_or_create(
                        user=buyer,
                        auction=auction,
                        defaults={'notify_before_end': random.choice([True, False])}
                    )
                    if created:
                        watchlist_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {watchlist_count} watchlist entries'))

        # =====================
        # 6. CREATE ESCROW FOR ENDED AUCTIONS
        # =====================
        if has_escrow:
            self.stdout.write('\n🔒 Creating escrow records for ended auctions...')
            
            ended_auctions = [a for a in auctions if a.end_time < now]
            escrow_count = 0
            
            for auction in ended_auctions:
                # Get highest bidder
                highest_bid = auction.bids.order_by('-amount').first()
                if highest_bid:
                    try:
                        escrow, created = Escrow.objects.get_or_create(
                            auction=auction,
                            defaults={
                                'buyer': highest_bid.user,
                                'seller': auction.owner,
                                'amount': highest_bid.amount,
                                'status': 'PENDING_PAYMENT',
                            }
                        )
                        if created:
                            escrow_count += 1
                    except Exception as e:
                        self.stdout.write(f'  ⚠ Escrow error: {e}')
            
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created {escrow_count} escrow records'))

        # =====================
        # SUMMARY
        # =====================
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))
        self.stdout.write('='*50)
        self.stdout.write('\n📋 Test Accounts:')
        self.stdout.write('   Admin:   admin / admin123')
        self.stdout.write('   Sellers: seller1, seller2, seller3 / password123')
        self.stdout.write('   Buyers:  buyer1, buyer2, buyer3, buyer4 / password123')
        self.stdout.write(f'\n📊 Data Created:')
        self.stdout.write(f'   • {len(categories)} Categories')
        self.stdout.write(f'   • {len(auctions)} Auctions ({len([a for a in auctions if a.is_active])} active)')
        self.stdout.write(f'   • {bid_count} Bids')
        self.stdout.write(f'   • {watchlist_count} Watchlist entries')
        self.stdout.write('')
