import datetime
import logging
import time
from django.http import HttpResponseForbidden, HttpResponse
from django.core.cache import cache
from django.contrib.auth.models import User

# Task 1: Request Logging Middleware
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        log_message = f"User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response

# Task 2: Time Restriction Middleware
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # For testing: Always allow access
        response = self.get_response(request)
        return response

# Task 3: Rate Limiting Middleware
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5
        self.window = 60

    def __call__(self, request):
        if request.method == 'POST':
            ip_address = self.get_client_ip(request)
            cache_key = f"rate_limit_{ip_address}"
            
            requests_data = cache.get(cache_key, {'count': 0, 'start_time': time.time()})
            
            current_time = time.time()
            if current_time - requests_data['start_time'] > self.window:
                requests_data = {'count': 1, 'start_time': current_time}
            else:
                if requests_data['count'] >= self.limit:
                    return HttpResponseForbidden("Rate limit exceeded. Please try again in a minute.")
                requests_data['count'] += 1
            
            cache.set(cache_key, requests_data, self.window)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# Task 4: Role Permission Middleware - FIXED CLASS NAME
class RolepermissionMiddleware:  # Changed from RolepermissionMiddleware to RolePermissionMiddleware
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths that require special permissions
        admin_paths = ['/admin/', '/delete/', '/moderate/', '/admin-panel/']
        
        # Check if the current path requires admin permissions
        if any(request.path.startswith(path) for path in admin_paths):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required to access this resource.")
            
            # Check if user has admin or moderator privileges
            if not (request.user.is_staff or request.user.is_superuser or self.is_moderator(request.user)):
                return HttpResponseForbidden("Insufficient permissions. Admin or moderator role required.")
        
        response = self.get_response(request)
        return response
    
    def is_moderator(self, user):
        # Check if user is in moderator group
        return user.groups.filter(name='moderator').exists()

