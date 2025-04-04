from django.contrib import admin
from django.urls import path
from .views import LoginView, RegistrationView, ActivateUserView, CheckEmailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registraion/', RegistrationView.as_view(), name='registration'),
    path('activate/', ActivateUserView.as_view(), name='activate'),
    path('check-email/', CheckEmailView.as_view(), name='check-email'),
]