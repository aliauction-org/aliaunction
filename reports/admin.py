from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "report_type",
        "reason",
        "reporter",
        "is_resolved",
        "created_at",
    )
    list_filter = ("report_type", "reason", "is_resolved")
    search_fields = ("description", "reporter__username")
