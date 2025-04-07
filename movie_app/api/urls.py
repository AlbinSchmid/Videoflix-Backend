from django.contrib import admin
from django.urls import path
from .views import *
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
    path('movies/', cache_page(CACHE_TTL)(MovieListView.as_view()), name='movies'),
]