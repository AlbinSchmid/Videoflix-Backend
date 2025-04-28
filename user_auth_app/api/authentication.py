from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication class that retrieves the token from cookies."""
    def authenticate(self, request):
        """Authenticate the user using the JWT token stored in cookies."""
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token