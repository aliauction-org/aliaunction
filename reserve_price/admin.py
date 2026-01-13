from django.contrib import admin
from .models import ReservePrice

@admin.register(ReservePrice)
class ReservePriceAdmin(admin.ModelAdmin):
    list_display = ('auction', 'amount', 'seller_only')
    search_fields = ('auction__title',)
