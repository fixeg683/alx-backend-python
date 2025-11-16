from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("api/")),
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),        # app routes
    path("api-auth/", include("rest_framework.urls")),  # ✅ add api-auth
]
