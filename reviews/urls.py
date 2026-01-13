from django.urls import path
from . import views

urlpatterns = [
    path("<int:escrow_id>/", views.leave_rating, name="leave_rating"),
]
