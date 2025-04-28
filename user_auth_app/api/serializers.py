from rest_framework import serializers
from user_auth_app.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from .exeptions import PasswordNotMatch, EmailExistAlready


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""
    class Meta:
        """Meta class to define the model and fields to be serialized."""
        model = CustomUser
        fields = ['id', 'email']


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    email = serializers.EmailField(required=True)
    repeated_password = serializers.CharField(required=True)

    class Meta:
        """Meta class to define the model and fields to be serialized."""
        model = CustomUser
        fields = ['email', 'password', 'repeated_password']

    def validate_email(self, value):
        """Validate the email field."""
        if CustomUser.objects.filter(email=value).exists():
            raise EmailExistAlready
        return value

    def validate(self, data):
        """Validate the data before saving."""
        if data['password'] != data['repeated_password']:
            raise PasswordNotMatch

        validate_password(data['password'])
        return data

    def save(self):
        """Save the user instance after validation."""
        password = self.validated_data['password']
        email = self.validated_data['email']

        account = CustomUser(email=email)
        account.set_password(password)
        account.save()
        return account
    

class EmailLogInSerializer(serializers.Serializer):
    """Serializer for user login using email."""
    email = serializers.EmailField()
    password = serializers.CharField()

        
