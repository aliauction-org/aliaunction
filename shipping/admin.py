from django.contrib import admin
from .models import ShippingDetail

@admin.register(ShippingDetail)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ("escrow", "city", "state", "postal_code", "delivery_charge")
