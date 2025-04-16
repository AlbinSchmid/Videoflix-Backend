from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .views import *

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/progress/', UserMovieProgressListView.as_view(), name='movie-progress'),
    path('movie/progress/<slug:slug>/', UserMovieProgressDetailView.as_view(), name='movie-progress-detail'),
]