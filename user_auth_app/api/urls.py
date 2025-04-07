from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registraion/', RegistrationView.as_view(), name='registration'),
    path('activate/', ActivateUserView.as_view(), name='activate'),
    path('check-email/', CheckEmailView.as_view(), name='check-email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('check-reset-password-token/', CheckPasswordToken.as_view(), name="check-password-token"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password")
]