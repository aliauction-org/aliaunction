from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),
    path('api/unread/', views.unread_notifications_api, name='unread_notifications_api'),
    path('api/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
] 