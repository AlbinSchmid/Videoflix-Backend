from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from user_auth_app.models import CustomUser
from .serializers import RegistrationSerializer, UserSerializer, EmailLogInSerializer
from .exeptions import *
from .permissions import IsLoggedIn
from rest_framework.throttling import ScopedRateThrottle
from .emails import send_password_reset_email
import django_rq


class CheckPasswordToken(APIView):
    """View to check if the password reset token is valid."""
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'password_reset'

    def post(self, request):
        """Check if the password reset token is valid."""
        uidb64 = request.data.get('uid')
        token = request.data.get('token')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise IncorrectUrl

        if not default_token_generator.check_token(user, token):
            raise IncorrectUrl
        return Response(status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """View to reset the password."""
    throttle_scope = 'password_reset'

    def post(self, request):
        """Reset the password."""
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')
        repeated_password = request.data.get('repeated_password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise IncorrectUrl

        if not user.is_active:
            raise NotVerifiedForgotPassword

        if not default_token_generator.check_token(user, token):
            raise IncorrectUrl

        if password != repeated_password:
            raise PasswordNotMatch

        if check_password(password, user.password):
            raise PasswordSameAsOld

        try:
            validate_password(password, user=user)
        except Exception as e:
            raise ValidationError({"password": list(e.messages)})

        user.set_password(password)
        user.save()
        return Response({"detail": "Your password was reset successfully. You can now log in with your new password."}, status=200)


class ForgotPasswordView(APIView):
    """View to handle password reset requests."""
    throttle_scope = 'password_reset'

    def post(self, request):
        """Handle password reset request."""
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            if user.is_active:
                queue = django_rq.get_queue('default', autocommit=True)
                queue.enqueue(send_password_reset_email, user)
                return Response({'message': 'We have sent you an email with instructions to reset your password.'}, status=200)
            raise NotVerifiedForgotPassword
        raise UserNotFound


class CheckEmailView(APIView):
    """View to check if the email exists in the database."""
    permission_classes = [AllowAny]
    def post(self, request):
        """Check if the email exists in the database."""
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).exists()

        if user:
            return Response(
                {'exist': True,
                 'message': 'This email is already registered. You have been redirected to the login page.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'exist': False},
                status=status.HTTP_200_OK
            )


class ActivateUserView(APIView):
    """View to activate the user account."""
    permission_classes = [AllowAny]
    throttle_scope = 'activation'

    def post(self, request):
        """Activate the user account."""
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise IncorrectUrl

        if user.is_active:
            raise UserAlreadyVerified

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Your account has been successfully verified. You can now log in and start using Videoflix.'}, status=status.HTTP_200_OK)
        raise IncorrectUrl


class ProtectedView(APIView):
    """View to check if the user is logged in."""
    permission_classes = [IsLoggedIn]

    def get(self, request):
        """Check if the user is logged in."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    """View to handle user logout."""
    throttle_scope = 'login'

    def post(self, request):
        """Handle user logout."""
        response = Response({"message": "Logout successful"})
        response.set_cookie(
            key='access_token',
            value='',     
            httponly=True,
            secure=True,
            samesite='None',
            max_age=0,  
            path='/',
        )
        return response


class CustomLogInView(APIView):
    """View for user login."""
    throttle_scope = 'login'
    
    def post(self, request):
        """Handle user login."""
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        userExist = CustomUser.objects.filter(email=email).exists()
        serializer = EmailLogInSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        if user:
            if not user.is_active:
                raise NotVerified

            refresh = RefreshToken.for_user(user)

            response = Response({'message': 'Login successful'})
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=False,  # True
                samesite='Lax',  # None
                max_age=60 * 60 * 24,
            )
            return response
        if userExist:
            raise IncorrectPassword
        raise UserNotExistWithThisEmail


class RegistrationView(APIView):
    """View for user registration."""
    throttle_classes = [ScopedRateThrottle]
    throttle_classes = 'registration'

    def post(self, request):
        """Register a new user"""
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Registration successful! Please check your email to verify your account before logging in.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




