"""
Rate limiting utilities for bid endpoint and login attempts.
Uses simple in-memory rate limiting. For production, consider django-ratelimit with Redis.
"""
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
import time


class RateLimiter:
    """Simple rate limiter using Django's cache framework."""
    
    def __init__(self, key_prefix, max_requests, window_seconds):
        self.key_prefix = key_prefix
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def get_cache_key(self, identifier):
        return f"rate_limit:{self.key_prefix}:{identifier}"
    
    def is_rate_limited(self, identifier):
        """Check if the identifier has exceeded the rate limit."""
        cache_key = self.get_cache_key(identifier)
        request_count = cache.get(cache_key, 0)
        
        if request_count >= self.max_requests:
            return True
        
        # Increment count
        if request_count == 0:
            cache.set(cache_key, 1, self.window_seconds)
        else:
            cache.incr(cache_key)
        
        return False
    
    def get_remaining(self, identifier):
        """Get remaining requests for identifier."""
        cache_key = self.get_cache_key(identifier)
        request_count = cache.get(cache_key, 0)
        return max(0, self.max_requests - request_count)


# Pre-configured rate limiters
bid_rate_limiter = RateLimiter(
    key_prefix="bid",
    max_requests=10,  # 10 bids per minute
    window_seconds=60
)

login_rate_limiter = RateLimiter(
    key_prefix="login",
    max_requests=5,  # 5 login attempts per minute
    window_seconds=60
)


def get_client_identifier(request):
    """Get a unique identifier for the client (IP or user ID)."""
    if request.user.is_authenticated:
        return f"user:{request.user.id}"
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    return f"ip:{ip}"


def rate_limit_bid(view_func):
    """
    Decorator to rate limit bid submissions.
    Allows 10 bids per minute per user/IP.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            identifier = get_client_identifier(request)
            
            if bid_rate_limiter.is_rate_limited(identifier):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': 'Too many bids. Please wait a moment before bidding again.',
                        'rate_limited': True
                    }, status=429)
                else:
                    messages.error(request, 'Too many bids. Please wait a moment before bidding again.')
                    return redirect(request.path)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def rate_limit_login(view_func):
    """
    Decorator to rate limit login attempts.
    Allows 5 attempts per minute per IP.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR', 'unknown')
            
            identifier = f"ip:{ip}"
            
            if login_rate_limiter.is_rate_limited(identifier):
                messages.error(request, 'Too many login attempts. Please wait a minute and try again.')
                return redirect(request.path)
        
        return view_func(request, *args, **kwargs)
    return wrapper
