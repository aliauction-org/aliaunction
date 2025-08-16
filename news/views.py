from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

from .models import Article, Category, Tag, Comment
from .forms import ArticleForm, CommentForm, ArticleSearchForm

def article_list(request):
    """Display list of published articles with search and filtering"""
    form = ArticleSearchForm(request.GET)
    articles = Article.objects.filter(status='published')
    
    # Apply search filters
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        tags = form.cleaned_data.get('tags')
        sort_by = form.cleaned_data.get('sort_by', 'newest')
        
        if q:
            articles = articles.filter(
                Q(title__icontains=q) | 
                Q(content__icontains=q) | 
                Q(excerpt__icontains=q)
            )
        
        if category:
            articles = articles.filter(category=category)
        
        if tags:
            articles = articles.filter(tags__in=tags).distinct()
        
        # Apply sorting
        if sort_by == 'oldest':
            articles = articles.order_by('published_at')
        elif sort_by == 'most_viewed':
            articles = articles.order_by('-views')
        elif sort_by == 'most_commented':
            articles = articles.annotate(comment_count=Count('comments')).order_by('-comment_count')
        else:  # newest
            articles = articles.order_by('-published_at')
    
    # Pagination
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get featured articles
    featured_articles = Article.objects.filter(status='published', is_featured=True)[:3]
    
    # Get categories and tags for sidebar
    categories = Category.objects.annotate(article_count=Count('articles'))
    popular_tags = Tag.objects.annotate(article_count=Count('articles')).order_by('-article_count')[:10]
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'featured_articles': featured_articles,
        'categories': categories,
        'popular_tags': popular_tags,
    }
    return render(request, 'news/article_list.html', context)

def article_detail(request, slug):
    """Display individual article with comments"""
    article = get_object_or_404(Article, slug=slug, status='published')
    
    # Increment view count
    article.increment_views()
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect(article.get_absolute_url())
    else:
        comment_form = CommentForm()
    
    # Get approved comments
    comments = article.comments.filter(is_approved=True, parent=None)
    
    # Get related articles
    related_articles = Article.objects.filter(
        status='published',
        category=article.category
    ).exclude(id=article.id)[:3]
    
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'related_articles': related_articles,
    }
    return render(request, 'news/article_detail.html', context)

def category_detail(request, slug):
    """Display articles by category"""
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category, status='published').order_by('-published_at')
    
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'news/category_detail.html', context)

def tag_detail(request, slug):
    """Display articles by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(tags=tag, status='published').order_by('-published_at')
    
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'news/tag_detail.html', context)

@login_required
def article_create(request):
    """Create a new article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Article created successfully!')
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
        'title': 'Create New Article',
    }
    return render(request, 'news/article_form.html', context)

@login_required
def article_edit(request, slug):
    """Edit an existing article"""
    article = get_object_or_404(Article, slug=slug)
    
    # Check if user is the author or admin
    if not (request.user == article.author or request.user.is_staff):
        messages.error(request, 'You do not have permission to edit this article.')
        return redirect(article.get_absolute_url())
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
        'article': article,
        'title': 'Edit Article',
    }
    return render(request, 'news/article_form.html', context)

@login_required
@require_POST
def comment_create(request, article_id):
    """Create a new comment via AJAX"""
    article = get_object_or_404(Article, id=article_id, status='published')
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Comment submitted successfully and is awaiting approval.',
            'comment': {
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })

def latest_news(request):
    """API endpoint for latest news (for footer)"""
    latest_articles = Article.objects.filter(
        status='published'
    ).order_by('-published_at')[:5]
    
    return JsonResponse({
        'articles': [
            {
                'title': article.title,
                'url': article.get_absolute_url(),
                'published_at': article.published_at.strftime('%B %d, %Y'),
            }
            for article in latest_articles
        ]
    })
