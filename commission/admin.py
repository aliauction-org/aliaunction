from django.contrib import admin
from .models import CommissionRule

@admin.register(CommissionRule)
class CommissionRuleAdmin(admin.ModelAdmin):
    list_display = ("seller_percent", "buyer_percent", "is_active", "created_at")

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            CommissionRule.objects.exclude(id=obj.id).update(is_active=False)
        super().save_model(request, obj, form, change)
