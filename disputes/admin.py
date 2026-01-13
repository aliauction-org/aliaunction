from django.contrib import admin
from .models import Dispute

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ("id", "auction", "raised_by", "issue_type", "status", "created_at")
    list_filter = ("status", "issue_type")
    search_fields = ("description", "auction__title", "raised_by__username")
