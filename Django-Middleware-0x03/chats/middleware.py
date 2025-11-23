import datetime
import logging
import time
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.contrib.auth.models import User

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        self.logger.info(f"User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(21, 0)  # 9 PM
        end_time = datetime.time(6, 0)     # 6 AM (next day)
        
        # Check if current time is outside allowed hours (9 PM to 6 AM)
        # If it's after 9 PM OR before 6 AM, allow access
        # If it's between 6 AM and 9 PM, deny access
        if current_time >= start_time or current_time <= end_time:
            # Allow access during 9 PM to 6 AM
            response = self.get_response(request)
            return response
        else:
            # Deny access between 6 AM and 9 PM
            return HttpResponseForbidden(
                "Access denied: Chat is only available between 9 PM and 6 AM. "
                f"Current time: {current_time.strftime('%H:%M')}"
            )

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5
        self.window = 60

    def __call__(self, request):
        if request.method == 'POST' and ('message' in request.path or 'messages' in request.path):
            ip_address = self.get_client_ip(request)
            cache_key = f"rate_limit_{ip_address}"
            
            requests_data = cache.get(cache_key, {'count': 0, 'start_time': time.time()})
            
            current_time = time.time()
            if current_time - requests_data['start_time'] > self.window:
                requests_data = {'count': 1, 'start_time': current_time}
                cache.set(cache_key, requests_data, self.window)
            else:
                if requests_data['count'] >= self.limit:
                    return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
                
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

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_paths = ['/admin/', '/admin-panel/', '/delete/', '/moderate/']
        
        if any(request.path.startswith(path) for path in admin_paths):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            
            if not (request.user.is_staff or request.user.is_superuser or self.is_moderator(request.user)):
                return HttpResponseForbidden("Insufficient permissions")
        
        response = self.get_response(request)
        return response
    
    def is_moderator(self, user):
        return user.groups.filter(name='moderator').exists()