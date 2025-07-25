from django.contrib import admin
from .models import Review, Rating

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'content', 'created_at')
    list_filter = ('auction', 'user')
    search_fields = ('auction__title', 'user__username', 'content')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'score', 'created_at')
    list_filter = ('auction', 'user')
    search_fields = ('auction__title', 'user__username')
