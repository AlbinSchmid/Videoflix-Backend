from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_auth_app.models import CustomUser
from .serializers import RegistrationSerializer, EmailLogInSerializer
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .exeptions import UserAlreadyVerified, IncorrectUrl, UserNotFound, NotVerifiedForgotPassword, PasswordNotMatch, PasswordSameAsOld
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

class CheckPasswordToken(APIView):
    def post(self, request):
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
    def post(self, request):
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

    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            if user.is_active:
                subject = 'Reset your Videoflix password'
                from_email = 'noreply@videoflix.de'
                to = [user.email]

                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"http://localhost:4200/reset-password/{uid}/{token}"

                html_content = render_to_string('emails/reset_password.html', {
                    'reset_link': reset_link
                })
                text_content = 'Hello, to reset your password pleace contact our Support'

                email = EmailMultiAlternatives(subject, text_content, from_email, to)
                email.attach_alternative(html_content, "text/html")
                email.send()
                return Response({'message': 'We have sent you an email with instructions to reset your password.'}, status=200)
            raise NotVerifiedForgotPassword
        raise UserNotFound


class CheckEmailView(APIView):
    def post(self, request):
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
    def post(self, request):
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


class LoginView(ObtainAuthToken):

    def post(self, request):
        serializer = EmailLogInSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'email': user.email,
                'id': user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'message': 'Registration successful! Please check your email to verify your account before logging in.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
