"""
URL configuration for the newsroom project.

This file defines the URL patterns for the project-level routing.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_room.urls')),  # this includes all app-level routes, including the new API ones
]

