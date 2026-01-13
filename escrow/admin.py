from django.contrib import admin
from .models import Escrow

@admin.register(Escrow)
class EscrowAdmin(admin.ModelAdmin):
    list_display = ("auction", "buyer", "seller", "status", "last_updated")
    list_filter = ("status",)
