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
from auctions.models import Auction
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone

def homepage(request):
    query = request.GET.get('search', '').strip()
    auctions = Auction.objects.filter(is_active=True)
    if query:
        auctions = auctions.filter(Q(title__icontains=query) | Q(description__icontains=query))
    auctions = auctions.order_by('-created_at')
    categories = Auction.objects.values('id', 'title').annotate(count=Count('id'))[:5]  # Placeholder for categories
    return render(request, 'home.html', {
        'auctions': auctions, 
        'categories': categories, 
        'search_query': query,
        'now': timezone.now()
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
    path('', homepage, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
