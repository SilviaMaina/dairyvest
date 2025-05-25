"""
URL configuration for dairyvest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# 👋 Root JSON welcome response
def welcome(request):
    return JsonResponse({
        "message": "Welcome to DairyVest API 👨🏾‍🌾💸",
        "routes": [
            "/api/auth/",
            "/api/sacco/",
            "/admin/"
        ]
    })

urlpatterns = [
    path('', welcome),  # /JSON message
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/sacco/', include('sacco.urls')),
]