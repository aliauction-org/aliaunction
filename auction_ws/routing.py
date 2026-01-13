from django.urls import re_path
from .consumers import AuctionUpdatesConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/auction/(?P<auction_id>\d+)/$",
        AuctionUpdatesConsumer.as_asgi(),
    ),
]
