from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Chat App! Request logged successfully.")

def messages_view(request):
    if request.method == 'POST':
        return HttpResponse("Message sent successfully!")
    return HttpResponse("Messages page - GET request")

def admin_panel_view(request):
    return HttpResponse("Admin panel - Access granted")

def delete_view(request):
    return HttpResponse("Delete function - Admin access required")

def moderate_view(request):
    return HttpResponse("Moderate function - Admin access required")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('messages/', messages_view, name='messages'),
    path('admin-panel/', admin_panel_view, name='admin-panel'),
    path('delete/', delete_view, name='delete'),
    path('moderate/', moderate_view, name='moderate'),
]
