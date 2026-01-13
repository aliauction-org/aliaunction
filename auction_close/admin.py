from django.contrib import admin
from .models import AuctionCloseMode

@admin.register(AuctionCloseMode)
class AuctionCloseModeAdmin(admin.ModelAdmin):
    list_display = ("auction", "mode")
    list_filter = ("mode",)
    search_fields = ("auction__title",)
