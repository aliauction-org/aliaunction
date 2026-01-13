from django.urls import path
from . import views

urlpatterns = [
    path("<int:escrow_id>/", views.add_shipping, name="add_shipping"),
]
