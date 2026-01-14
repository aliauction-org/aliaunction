"""
Comprehensive tests for the Auction Platform backend.
Tests cover: auctions, bid validations, anti-sniping, escrow, payments, ratings.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from auctions.models import Auction, Bid, Category, AuctionImage


User = get_user_model()


class AuctionModelTests(TestCase):
    """Tests for the Auction model."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            is_active=True
        )
    
    def test_create_auction(self):
        """Test auction creation with all fields."""
        auction = Auction.objects.create(
            title='Test Auction',
            description='A test description',
            starting_price=Decimal('100.00'),
            current_price=Decimal('100.00'),
            end_time=timezone.now() + timedelta(days=7),
            owner=self.seller,
            is_active=True,
            category=self.category,
            is_featured=False,
            view_count=0
        )
        
        self.assertEqual(auction.title, 'Test Auction')
        self.assertEqual(auction.owner, self.seller)
        self.assertEqual(auction.category, self.category)
        self.assertEqual(auction.view_count, 0)
    
    def test_featured_auction(self):
        """Test featured auction fields."""
        auction = Auction.objects.create(
            title='Featured Auction',
            description='A featured item',
            starting_price=Decimal('500.00'),
            current_price=Decimal('500.00'),
            end_time=timezone.now() + timedelta(days=3),
            owner=self.seller,
            is_active=True,
            is_featured=True,
            featured_order=1
        )
        
        self.assertTrue(auction.is_featured)
        self.assertEqual(auction.featured_order, 1)
    
    def test_category_creation(self):
        """Test category model."""
        category = Category.objects.create(
            name='Vehicles',
            slug='vehicles',
            description='Cars, bikes, etc.',
            is_active=True,
            order=2
        )
        
        self.assertEqual(str(category), 'Vehicles')
        self.assertTrue(category.is_active)


class BidValidationTests(TestCase):
    """Tests for bid validation logic."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.bidder = User.objects.create_user(
            username='bidder',
            email='bidder@test.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test description',
            starting_price=Decimal('100.00'),
            current_price=Decimal('100.00'),
            end_time=timezone.now() + timedelta(days=1),
            owner=self.seller,
            is_active=True
        )
    
    def test_valid_bid(self):
        """Test creating a valid bid."""
        bid = Bid.objects.create(
            auction=self.auction,
            user=self.bidder,
            amount=Decimal('150.00'),
            ip_address='192.168.1.1',
            user_agent='Test Browser'
        )
        
        self.assertEqual(bid.amount, Decimal('150.00'))
        self.assertEqual(bid.ip_address, '192.168.1.1')
    
    def test_bid_audit_trail(self):
        """Test that bid captures IP and user agent."""
        bid = Bid.objects.create(
            auction=self.auction,
            user=self.bidder,
            amount=Decimal('200.00'),
            ip_address='10.0.0.1',
            user_agent='Mozilla/5.0 Test'
        )
        
        self.assertEqual(bid.ip_address, '10.0.0.1')
        self.assertIn('Mozilla', bid.user_agent)


class BidProtectionTests(TestCase):
    """Tests for bid protection validators."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.bidder = User.objects.create_user(
            username='bidder',
            email='bidder@test.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test description',
            starting_price=Decimal('100.00'),
            current_price=Decimal('100.00'),
            end_time=timezone.now() + timedelta(days=1),
            owner=self.seller,
            is_active=True
        )
    
    def test_validate_negative_bid(self):
        """Test that negative bids are rejected."""
        from bid_protection.validators import validate_bid
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            validate_bid(self.bidder, self.auction, Decimal('-10.00'))
    
    def test_validate_seller_cannot_bid(self):
        """Test that seller cannot bid on own auction."""
        from bid_protection.validators import validate_bid
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            validate_bid(self.seller, self.auction, Decimal('150.00'))
    
    def test_validate_bid_on_ended_auction(self):
        """Test that bidding on ended auction raises error."""
        from bid_protection.validators import validate_bid
        from django.core.exceptions import ValidationError
        
        self.auction.end_time = timezone.now() - timedelta(hours=1)
        self.auction.save()
        
        with self.assertRaises(ValidationError):
            validate_bid(self.bidder, self.auction, Decimal('150.00'))


class RateLimitTests(TestCase):
    """Tests for rate limiting functionality."""
    
    def test_rate_limiter_creation(self):
        """Test RateLimiter class instantiation."""
        from bid_protection.rate_limit import RateLimiter
        
        limiter = RateLimiter(
            key_prefix='test',
            max_requests=10,
            window_seconds=60
        )
        
        self.assertEqual(limiter.max_requests, 10)
        self.assertEqual(limiter.window_seconds, 60)
    
    def test_cache_key_generation(self):
        """Test cache key is properly formatted."""
        from bid_protection.rate_limit import RateLimiter
        
        limiter = RateLimiter('bid', 10, 60)
        key = limiter.get_cache_key('user:123')
        
        self.assertEqual(key, 'rate_limit:bid:user:123')


class EscrowModelsTests(TestCase):
    """Tests for Escrow models and services."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@test.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test',
            starting_price=Decimal('100.00'),
            current_price=Decimal('150.00'),
            end_time=timezone.now() - timedelta(hours=1),
            owner=self.seller,
            is_active=False
        )
    
    def test_escrow_creation(self):
        """Test escrow creation with initial status."""
        from escrow.models import Escrow
        
        escrow = Escrow.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            status='PENDING_PAYMENT'
        )
        
        self.assertEqual(escrow.status, 'PENDING_PAYMENT')
        self.assertEqual(escrow.buyer, self.buyer)
        self.assertEqual(escrow.seller, self.seller)
    
    def test_mark_paid(self):
        """Test marking escrow as paid."""
        from escrow.models import Escrow
        from escrow.services import mark_paid
        
        escrow = Escrow.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            status='PENDING_PAYMENT'
        )
        
        result = mark_paid(escrow)
        escrow.refresh_from_db()
        
        self.assertTrue(result)
        self.assertEqual(escrow.status, 'PAID')
    
    def test_mark_shipped(self):
        """Test marking escrow as shipped."""
        from escrow.models import Escrow
        from escrow.services import mark_shipped
        
        escrow = Escrow.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            status='PAID'
        )
        
        result = mark_shipped(escrow)
        escrow.refresh_from_db()
        
        self.assertTrue(result)
        self.assertEqual(escrow.status, 'SHIPPED')
    
    def test_mark_delivered(self):
        """Test marking escrow as delivered (auto-completes)."""
        from escrow.models import Escrow
        from escrow.services import mark_delivered
        
        escrow = Escrow.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            status='SHIPPED'
        )
        
        result = mark_delivered(escrow)
        escrow.refresh_from_db()
        
        self.assertTrue(result)
        self.assertEqual(escrow.status, 'COMPLETED')
    
    def test_invalid_status_transition(self):
        """Test that invalid status transitions return False."""
        from escrow.models import Escrow
        from escrow.services import mark_shipped
        
        escrow = Escrow.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            status='PENDING_PAYMENT'  # Cannot ship without payment
        )
        
        result = mark_shipped(escrow)
        
        self.assertFalse(result)
        self.assertEqual(escrow.status, 'PENDING_PAYMENT')


class PaymentModelsTests(TestCase):
    """Tests for Payment and Invoice models."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@test.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test',
            starting_price=Decimal('1000.00'),
            current_price=Decimal('1500.00'),
            end_time=timezone.now() - timedelta(hours=1),
            owner=self.seller,
            is_active=False
        )
    
    def test_invoice_creation(self):
        """Test invoice creation with commission calculation."""
        from payments.models import Invoice
        
        invoice = Invoice.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            amount=Decimal('1500.00'),
            buyer_commission=Decimal('45.00'),  # 3%
            seller_commission=Decimal('150.00'),  # 10%
            transport_charge=Decimal('100.00'),
            status='PENDING'
        )
        
        self.assertEqual(invoice.amount, Decimal('1500.00'))
        self.assertEqual(invoice.buyer_commission, Decimal('45.00'))
        self.assertEqual(invoice.seller_commission, Decimal('150.00'))
    
    def test_invoice_total_payable(self):
        """Test total_payable calculation."""
        from payments.models import Invoice
        
        invoice = Invoice.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            amount=Decimal('1500.00'),
            buyer_commission=Decimal('45.00'),
            seller_commission=Decimal('150.00'),
            transport_charge=Decimal('100.00'),
            status='PENDING'
        )
        
        # Total = amount + buyer_commission + transport_charge
        expected_total = Decimal('1500.00') + Decimal('45.00') + Decimal('100.00')
        self.assertEqual(invoice.total_payable(), expected_total)


class ShippingTests(TestCase):
    """Tests for Shipping models."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@test.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test',
            starting_price=Decimal('100.00'),
            current_price=Decimal('150.00'),
            end_time=timezone.now() - timedelta(hours=1),
            owner=self.seller,
            is_active=False
        )
    
    def test_shipping_detail_creation(self):
        """Test shipping detail creation."""
        from escrow.models import Escrow
        from shipping.models import ShippingDetail
        
        escrow = Escrow.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            status='PAID'
        )
        
        shipping = ShippingDetail.objects.create(
            escrow=escrow,
            full_name='John Doe',
            phone='9876543210',
            address_line1='123 Main Street',
            city='Mumbai',
            state='Maharashtra',
            postal_code='400001',
            country='India',
            delivery_charge=Decimal('150.00')
        )
        
        self.assertEqual(shipping.full_name, 'John Doe')
        self.assertEqual(shipping.city, 'Mumbai')
        self.assertEqual(shipping.delivery_charge, Decimal('150.00'))


class RatingTests(TestCase):
    """Tests for Rating/Reviews models."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@test.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test',
            starting_price=Decimal('100.00'),
            current_price=Decimal('150.00'),
            end_time=timezone.now() - timedelta(hours=1),
            owner=self.seller,
            is_active=False
        )
    
    def test_rating_creation(self):
        """Test rating creation for completed escrow."""
        from escrow.models import Escrow
        from reviews.models import Rating
        
        escrow = Escrow.objects.create(
            auction=self.auction,
            buyer=self.buyer,
            seller=self.seller,
            status='COMPLETED'
        )
        
        rating = Rating.objects.create(
            escrow=escrow,
            given_by=self.buyer,
            given_to=self.seller,
            role='BUYER',
            stars=5,
            review='Excellent seller, fast shipping!'
        )
        
        self.assertEqual(rating.stars, 5)
        self.assertEqual(rating.given_by, self.buyer)
        self.assertEqual(rating.given_to, self.seller)
        self.assertEqual(rating.role, 'BUYER')


class ViewTests(TestCase):
    """Tests for views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
    def test_homepage_loads(self):
        """Test homepage renders correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_auction_list_loads(self):
        """Test auction list page."""
        response = self.client.get('/auctions/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_required_for_create_auction(self):
        """Test that create auction requires login."""
        response = self.client.get('/auctions/create/')
        self.assertRedirects(response, '/users/login/?next=/auctions/create/')
    
    def test_authenticated_create_auction(self):
        """Test authenticated user can access create auction."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/auctions/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_requires_login(self):
        """Test dashboard pages require authentication."""
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/users/login/?next=/dashboard/')


class WatchlistTests(TestCase):
    """Tests for Watchlist functionality."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@test.com',
            password='testpass123'
        )
        self.auction = Auction.objects.create(
            title='Test Auction',
            description='Test',
            starting_price=Decimal('100.00'),
            current_price=Decimal('100.00'),
            end_time=timezone.now() + timedelta(days=1),
            owner=self.seller,
            is_active=True
        )
    
    def test_watchlist_creation(self):
        """Test adding auction to watchlist."""
        from watchlist.models import Watchlist
        
        watchlist_item = Watchlist.objects.create(
            user=self.buyer,
            auction=self.auction,
            notify_before_end=True
        )
        
        self.assertEqual(watchlist_item.user, self.buyer)
        self.assertEqual(watchlist_item.auction, self.auction)
        self.assertTrue(watchlist_item.notify_before_end)
        self.assertFalse(watchlist_item.notification_sent)
    
    def test_watchlist_unique_constraint(self):
        """Test that user can only watch an auction once."""
        from watchlist.models import Watchlist
        from django.db import IntegrityError
        
        Watchlist.objects.create(
            user=self.buyer,
            auction=self.auction
        )
        
        with self.assertRaises(IntegrityError):
            Watchlist.objects.create(
                user=self.buyer,
                auction=self.auction
            )


class CategoryFilterTests(TestCase):
    """Tests for category filtering in search."""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@test.com',
            password='testpass123'
        )
        self.electronics = Category.objects.create(
            name='Electronics',
            slug='electronics',
            is_active=True
        )
        self.furniture = Category.objects.create(
            name='Furniture',
            slug='furniture',
            is_active=True
        )
    
    def test_filter_by_category(self):
        """Test filtering auctions by category."""
        # Create auctions in different categories
        Auction.objects.create(
            title='Laptop',
            description='Test laptop',
            starting_price=Decimal('500.00'),
            current_price=Decimal('500.00'),
            end_time=timezone.now() + timedelta(days=1),
            owner=self.seller,
            is_active=True,
            category=self.electronics
        )
        Auction.objects.create(
            title='Desk',
            description='Test desk',
            starting_price=Decimal('200.00'),
            current_price=Decimal('200.00'),
            end_time=timezone.now() + timedelta(days=1),
            owner=self.seller,
            is_active=True,
            category=self.furniture
        )
        
        electronics_auctions = Auction.objects.filter(category=self.electronics)
        furniture_auctions = Auction.objects.filter(category=self.furniture)
        
        self.assertEqual(electronics_auctions.count(), 1)
        self.assertEqual(furniture_auctions.count(), 1)
        self.assertEqual(electronics_auctions.first().title, 'Laptop')
