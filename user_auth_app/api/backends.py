from django.contrib.auth.backends import ModelBackend
from user_auth_app.models import CustomUser

class EmailBackend(ModelBackend):
    """Custom authentication backend that allows login using email."""
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user using email or username and password.
        If the username is not provided, it will use the email field.
        """
        email = kwargs.get('email') or username
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None