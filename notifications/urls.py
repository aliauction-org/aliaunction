from django.urls import path
from . import views

urlpatterns = [
    path('api/unread/', views.unread_notifications_api, name='unread_notifications_api'),
    path('api/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
] 