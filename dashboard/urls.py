from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('my-auctions/', views.my_auctions, name='my_auctions'),
    path('my-bids/', views.my_bids, name='my_bids'),
]
