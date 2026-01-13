from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.start_verification, name="start_verification"),
    path("otp/", views.verify_otp, name="verify_otp"),
    path("status/", views.verification_status, name="verification_status"),
]
path("seller-verification/", include("seller_verification.urls")),
