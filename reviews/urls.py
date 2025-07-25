from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:auction_id>/', views.submit_review, name='submit_review'),
    path('auction/<int:auction_id>/', views.auction_reviews, name='auction_reviews'),
] 