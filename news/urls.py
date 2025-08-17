from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('create/', views.article_create, name='article_create'),
    path('edit/<slug:slug>/', views.article_edit, name='article_edit'),
    path('comment/<int:article_id>/', views.comment_create, name='comment_create'),
    path('api/latest/', views.latest_news, name='latest_news'),
] 