"""
Rate limiting middleware and decorators for AuctionVistas.
Provides simple in-memory rate limiting for bids and login attempts.
"""
import time
from functools import wraps
from django.http import JsonResponse
from django.shortcuts import render


class RateLimitStore:
    """Simple in-memory rate limit storage."""
    _store = {}
    
    @classmethod
    def get_key(cls, identifier, endpoint):
        return f"{endpoint}:{identifier}"
    
    @classmethod
    def check_rate_limit(cls, identifier, endpoint, max_requests, window_seconds):
        """
        Check if a request should be rate limited.
        Returns (is_allowed, remaining, reset_time)
        """
        key = cls.get_key(identifier, endpoint)
        current_time = time.time()
        
        if key not in cls._store:
            cls._store[key] = {
                'requests': [],
                'window_start': current_time
            }
        
        # Clean old requests outside the window
        cls._store[key]['requests'] = [
            t for t in cls._store[key]['requests']
            if current_time - t < window_seconds
        ]
        
        request_count = len(cls._store[key]['requests'])
        
        if request_count >= max_requests:
            # Rate limited
            oldest_request = min(cls._store[key]['requests'])
            reset_time = oldest_request + window_seconds
            return False, 0, reset_time
        
        # Add this request
        cls._store[key]['requests'].append(current_time)
        remaining = max_requests - request_count - 1
        reset_time = current_time + window_seconds
        
        return True, remaining, reset_time
    
    @classmethod
    def clear(cls):
        """Clear all rate limit data (for testing)."""
        cls._store = {}


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def rate_limit(max_requests=10, window_seconds=60, key_func=None):
    """
    Rate limiting decorator for views.
    
    Args:
        max_requests: Maximum number of requests allowed in the time window
        window_seconds: Time window in seconds
        key_func: Optional function to extract rate limit key from request
                  Default uses IP address
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get identifier for rate limiting
            if key_func:
                identifier = key_func(request)
            else:
                # Use IP + user ID if authenticated
                ip = get_client_ip(request)
                if request.user.is_authenticated:
                    identifier = f"{ip}:user:{request.user.id}"
                else:
                    identifier = ip
            
            # Get endpoint name
            endpoint = f"{view_func.__module__}.{view_func.__name__}"
            
            # Check rate limit
            is_allowed, remaining, reset_time = RateLimitStore.check_rate_limit(
                identifier, endpoint, max_requests, window_seconds
            )
            
            if not is_allowed:
                wait_time = int(reset_time - time.time())
                
                # Return JSON for AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': 'rate_limited',
                        'message': f'Too many requests. Please wait {wait_time} seconds.',
                        'retry_after': wait_time
                    }, status=429)
                
                # Return HTML for regular requests
                from django.contrib import messages
                messages.error(request, f'Too many attempts. Please wait {wait_time} seconds before trying again.')
                
                # For login, redirect back to login page
                if 'login' in endpoint.lower():
                    from django.shortcuts import redirect
                    return redirect('login')
                
                # For other endpoints, just show the error
                return render(request, 'rate_limited.html', {
                    'wait_time': wait_time,
                    'retry_after': reset_time
                }, status=429)
            
            # Add rate limit headers to response
            response = view_func(request, *args, **kwargs)
            response['X-RateLimit-Limit'] = str(max_requests)
            response['X-RateLimit-Remaining'] = str(remaining)
            response['X-RateLimit-Reset'] = str(int(reset_time))
            
            return response
        return wrapper
    return decorator


# Specific rate limiters for common endpoints
def rate_limit_bids(view_func):
    """Rate limit for bid submissions: 20 bids per minute per user."""
    return rate_limit(max_requests=20, window_seconds=60)(view_func)


def rate_limit_login(view_func):
    """Rate limit for login attempts: 5 attempts per minute per IP."""
    return rate_limit(max_requests=5, window_seconds=60)(view_func)


def rate_limit_api(view_func):
    """Rate limit for API endpoints: 60 requests per minute."""
    return rate_limit(max_requests=60, window_seconds=60)(view_func)
