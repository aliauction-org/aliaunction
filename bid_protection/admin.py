from django.contrib import admin
from .models import UserStatus

@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_suspended', 'updated_at')
    list_filter = ('is_suspended',)
    search_fields = ('user__username',)
