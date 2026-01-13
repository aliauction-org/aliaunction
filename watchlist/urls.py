from django.urls import path
from . import views

urlpatterns = [
    path("toggle/<int:auction_id>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("my/", views.my_watchlist, name="my_watchlist"),
]
