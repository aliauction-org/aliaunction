from django.urls import path
from . import views

urlpatterns = [
    path("<int:escrow_id>/", views.escrow_status, name="escrow_status"),
    path("<int:escrow_id>/ship/", views.mark_shipped_view, name="mark_shipped"),
    path("<int:escrow_id>/deliver/", views.mark_delivered_view, name="mark_delivered"),
]
