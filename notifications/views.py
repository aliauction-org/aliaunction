from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.

@login_required
def unread_notifications_api(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    data = [
        {
            'id': n.id,
            'message': n.message,
            'auction_id': n.auction.id if n.auction else None,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for n in notifications
    ]
    return JsonResponse({'notifications': data})

@login_required
def mark_notification_read(request, notification_id):
    Notification.objects.filter(id=notification_id, user=request.user).update(is_read=True)
    return JsonResponse({'success': True})
