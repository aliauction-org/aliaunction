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


@login_required
def notifications_list(request):
    """Display all notifications for the user."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def mark_all_as_read(request):
    """Mark all notifications as read for the current user."""
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        from django.contrib import messages
        messages.success(request, 'All notifications marked as read.')
    from django.shortcuts import redirect
    return redirect('notifications_list')

