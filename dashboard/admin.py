from django.contrib import admin
from .models import AdminCommission, AuctionApproval

@admin.register(AdminCommission)
class AdminCommissionAdmin(admin.ModelAdmin):
    list_display = ('auction', 'commission_amount', 'created_at')
    list_filter = ('auction',)
    search_fields = ('auction__title',)

@admin.register(AuctionApproval)
class AuctionApprovalAdmin(admin.ModelAdmin):
    list_display = ('auction', 'is_approved', 'reviewed_at')
    list_filter = ('is_approved',)
    search_fields = ('auction__title',)
