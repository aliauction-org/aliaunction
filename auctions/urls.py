from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('create/', views.create_auction, name='create_auction'),
    path('<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('api/status/<int:auction_id>/', views.auction_status_api, name='auction_status_api'),
] 