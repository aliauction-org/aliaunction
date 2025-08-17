from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('live-auctions/', views.live_auctions, name='live_auctions'),
    path('upcoming-items/', views.upcoming_items, name='upcoming_items'),
    path('sell-with-us/', views.sell_with_us, name='sell_with_us'),
    path('categories/', views.categories, name='categories'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('help-center/', views.help_center, name='help_center'),
    path('buyer-seller-guides/', views.buyer_seller_guides, name='buyer_seller_guides'),
    path('safe-bidding-tips/', views.safe_bidding_tips, name='safe_bidding_tips'),
    path('contact-support/', views.contact_support, name='contact_support'),
    path('terms-privacy/', views.terms_privacy, name='terms_privacy'),
] 