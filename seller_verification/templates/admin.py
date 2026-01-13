from django.contrib import admin
from .models import SellerVerification

@admin.register(SellerVerification)
class SellerVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_verified",
        "admin_verified",
        "created_at",
    )
    list_filter = ("phone_verified", "admin_verified")
