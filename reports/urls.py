from django.urls import path
from . import views

urlpatterns = [
    path("auction/<int:auction_id>/", views.report_auction, name="report_auction"),
    path("user/<int:user_id>/", views.report_user, name="report_user"),
]

path("report/", include("reports.urls")),
