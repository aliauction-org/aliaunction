from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from auctions.models import Auction, Category, Bid
from auction_workflow.models import AuctionWorkflow

User = get_user_model()

class FrontendFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='password123')
        self.seller = User.objects.create_user(username='seller', password='password123')
        
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        
        self.auction = Auction.objects.create(
            owner=self.seller,
            title='Test iPhone',
            description='A test phone',
            starting_price=10000,
            current_price=10000,
            end_time=timezone.now() + timezone.timedelta(days=1),
            category=self.category,
            is_featured=True
        )
        AuctionWorkflow.objects.create(auction=self.auction, status='APPROVED')

    def test_homepage_elements(self):
        """Test homepage renders with key elements and featured badge."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        
        # Check for Category filter
        self.assertIn('Electronics', content)
        
        # Check for Auction card
        self.assertIn('Test iPhone', content)
        
        # Check for Featured Badge
        self.assertIn('Featured', content)
        self.assertIn('featured-badge', content)

    def test_auction_detail_elements(self):
        """Test detail page for gallery, watchlist, and bid section."""
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('auction_detail', args=[self.auction.id]))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        
        # Check for Image Gallery structure
        self.assertIn('auction-image-section', content)
        
        # Check for Watchlist button (since logged in)
        self.assertIn('Add to Watchlist', content)
        
        # Check for Bid Form
        self.assertIn('Place Your Bid', content)
        
        # Check for Featured Badge on detail page
        self.assertIn('Featured', content)

    def test_dashboard_links(self):
        """Test that navigation includes dashboard links when logged in."""
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')
        
        self.assertIn('My Dashboard', content)
        self.assertIn('href="/dashboard/"', content) # Assuming reverse('dashboard_home') is /dashboard/

    def test_dashboard_pages(self):
        """Test that dashboard pages render correctly."""
        self.client.login(username='tester', password='password123')
        
        # Home
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('My Bids', response.content.decode('utf-8'))
        self.assertIn('My Auctions', response.content.decode('utf-8'))
        
        # My Bids
        response = self.client.get(reverse('my_bids'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('My Bids', response.content.decode('utf-8'))
