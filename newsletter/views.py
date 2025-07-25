from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import NewsletterSubscriber

# Create your views here.

@require_POST
def newsletter_signup(request):
    email = request.POST.get('email')
    if email:
        if not NewsletterSubscriber.objects.filter(email=email).exists():
            NewsletterSubscriber.objects.create(email=email)
            messages.success(request, 'Thank you for subscribing to AuctionVistas updates!')
        else:
            messages.info(request, 'You are already subscribed!')
    else:
        messages.error(request, 'Please enter a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', '/'))
