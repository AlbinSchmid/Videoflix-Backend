from django.contrib import admin
from django.urls import path
from .views import LoginView, RegistrationView, ActivateUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registraion/', RegistrationView.as_view(), name='registration'),
    path('activate/', ActivateUserView.as_view(), name='acitvate'),
]