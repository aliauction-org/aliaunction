from django.urls import path
from . import views

urlpatterns = [
    path("raise/<int:auction_id>/", views.raise_dispute, name="raise_dispute"),
    path("my/", views.my_disputes, name="my_disputes"),
]
