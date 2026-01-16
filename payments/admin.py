from django.contrib import admin
from .models import Payment, Refund, PlatformPaymentDetails, UserPaymentProfile, PaymentProof, Invoice, InvoicePayment
from django.utils import timezone
from escrows.models import Escrow

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction', 'amount', 'status', 'timestamp')
    list_filter = ('status', 'auction', 'user')
    search_fields = ('auction__title', 'user__username')

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('payment', 'amount', 'status', 'timestamp')
    list_filter = ('status',)

def verify_payment(modeladmin, request, queryset):
    for payment in queryset:
        payment.status = 'verified'
        payment.verified_by = request.user
        payment.verified_at = timezone.now()
        payment.save()

try:
            invoice = Invoice.objects.get(auction=proof.auction)
            invoice.status = "PAID"
            invoice.is_paid = True
            invoice.save(update_fields=["status", "is_paid"])
        except Invoice.DoesNotExist:
            pass

        # ✅ Mark escrow as paid (if exists)
        try:
            escrow = Escrow.objects.get(auction=proof.auction)
            escrow.status = "PAID"
            escrow.save(update_fields=["status"])
        except Escrow.DoesNotExist:
            pass
            
verify_payment.short_description = "Verify selected payments (mark Invoice+Escrow PAID)"

def reject_payment(modeladmin, request, queryset):
    queryset.update(status='rejected')
reject_payment.short_description = "Reject selected payments"

@admin.register(PlatformPaymentDetails)
class PlatformPaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_holder_name', 'account_number', 'updated_at')
    readonly_fields = ('updated_at',)

@admin.register(UserPaymentProfile)
class UserPaymentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_name', 'account_holder_name', 'account_number', 'created_at')
    search_fields = ('user__username', 'bank_name', 'account_holder_name')

@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display = ('auction', 'payer', 'payee', 'amount', 'direction', 'status', 'created_at')
    list_filter = ('status', 'direction', 'auction')
    search_fields = ('auction__title', 'payer__username', 'payee__username')
    actions = [verify_payment, reject_payment]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "auction", "buyer", "seller", "amount", "is_paid")
