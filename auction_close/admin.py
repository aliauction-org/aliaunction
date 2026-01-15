from django.contrib import admin
from .models import AuctionCloseMode, AntiSnipingSettings, GlobalAuctionSettings


@admin.register(AuctionCloseMode)
class AuctionCloseModeAdmin(admin.ModelAdmin):
    list_display = ("auction", "mode")
    list_filter = ("mode",)
    search_fields = ("auction__title",)


@admin.register(AntiSnipingSettings)
class AntiSnipingSettingsAdmin(admin.ModelAdmin):
    list_display = ("auction", "is_enabled", "threshold_minutes", "extension_minutes", "extensions_used", "max_extensions")
    list_filter = ("is_enabled",)
    search_fields = ("auction__title",)
    list_editable = ("is_enabled", "threshold_minutes", "extension_minutes")


@admin.register(GlobalAuctionSettings)
class GlobalAuctionSettingsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "default_anti_sniping_enabled", "default_threshold_minutes", "default_extension_minutes", "default_close_mode")
    
    def has_add_permission(self, request):
        # Only allow one instance
        if GlobalAuctionSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False

