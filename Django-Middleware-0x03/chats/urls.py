from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Chat App!")

def messages_view(request):
    if request.method == 'POST':
        return HttpResponse("Message sent!")
    return HttpResponse("Messages page")

def admin_view(request):
    return HttpResponse("Admin panel")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('messages/', messages_view, name='messages'),
    path('admin-panel/', admin_view, name='admin-panel'),
]