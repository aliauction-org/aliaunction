from django.db import models
from users.models import User

# Create your models here.


class Category(models.Model):
    """Auction category for filtering"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=20, decimal_places=2)
    current_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)
    
    # Category support
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='auctions'
    )
    
    # Featured auction support
    is_featured = models.BooleanField(default=False)
    featured_order = models.IntegerField(default=0)
    banner_image = models.ImageField(upload_to='auction_banners/', null=True, blank=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    @property
    def highest_bid(self):
        return self.bids.order_by('-amount', '-timestamp').first()
    
    def __str__(self):
        return self.title


class AuctionImage(models.Model):
    """Multiple images per auction for gallery feature"""
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='auction_gallery/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image for {self.auction.title}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Audit trail fields
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-amount', '-timestamp']
    
    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.auction.title}"


class ProxyBid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='proxy_bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proxy_bids')
    max_bid = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Proxy bid by {self.user.username} up to {self.max_bid}"

