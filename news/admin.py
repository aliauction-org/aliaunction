from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Article, Category, Tag, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views', 'published_at', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'tags', 'published_at', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    filter_horizontal = ['tags']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'tags', 'status')
        }),
        ('Settings', {
            'fields': ('is_featured', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')
    
    def save_model(self, request, obj, form, change):
        if not change:  # New article
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'article', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'article__category']
    search_fields = ['author__username', 'content', 'article__title']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_comments', 'disapprove_comments']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments have been approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def disapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments have been disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'
