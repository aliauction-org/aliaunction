"""
URL configuration for aliaunction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from auctions.models import Auction, Category
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone

def homepage(request):
    from watchlist.models import Watchlist
    
    query = request.GET.get('search', '').strip()
    category_slug = request.GET.get('category', '').strip()
    
    auctions = Auction.objects.filter(is_active=True)
    
    if query:
        auctions = auctions.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    if category_slug:
        auctions = auctions.filter(category__slug=category_slug)
        
    auctions = auctions.order_by('-created_at')
    
    # Get active categories with auction counts
    categories = Category.objects.filter(is_active=True).annotate(
        count=Count('auctions', filter=Q(auctions__is_active=True))
    ).order_by('order', 'name')
    
    # Get user's watchlist IDs for showing heart icons
    watchlist_ids = []
    if request.user.is_authenticated:
        watchlist_ids = list(Watchlist.objects.filter(user=request.user).values_list('auction_id', flat=True))
    
    return render(request, 'home.html', {
        'auctions': auctions, 
        'categories': categories, 
        'search_query': query,
        'selected_category': category_slug,
        'now': timezone.now(),
        'watchlist_ids': watchlist_ids,
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('auctions/', include('auctions.urls')),
    path('reviews/', include('reviews.urls')),
    path('contact/', include('contact.urls')),
    path('notifications/', include('notifications.urls')),
    path('payments/', include('payments.urls')),
    path('newsletter-signup/', include('newsletter.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('news/', include('news.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('watchlist/', include('watchlist.urls')),
    path('discover/', include('auction_discovery.urls')),
    path('reports/', include('reports.urls')),
    path('verification/', include('seller_verification.urls')),
    path('escrow/', include('escrow.urls')),
    path('shipping/', include('shipping.urls')),
    path('disputes/', include('disputes.urls')),
    path('ratings/', include('reviews.urls')),
    path('', homepage, name='home'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
