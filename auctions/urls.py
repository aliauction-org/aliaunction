from django.urls import path
from . import views
from .bulk_upload import bulk_upload_auctions, download_csv_template

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('create/', views.create_auction, name='create_auction'),
    path('bulk-upload/', bulk_upload_auctions, name='bulk_upload_auctions'),
    path('bulk-upload/template/', download_csv_template, name='download_csv_template'),
    path('<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('place-bid/<int:auction_id>/', views.auction_detail, name='place_bid'),
    path('api/status/<int:auction_id>/', views.auction_status_api, name='auction_status_api'),
]
 