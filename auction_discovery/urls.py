from django.urls import path
from .views import discover_auctions

urlpatterns = [
    path("", discover_auctions, name="discover_auctions"),
]
path("discover/", include("auction_discovery.urls")),
