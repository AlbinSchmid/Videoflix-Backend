from rest_framework import serializers
from user_auth_app.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from .exeptions import PasswordNotMatch, EmailExistAlready


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    repeated_password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'repeated_password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise EmailExistAlready
        return value

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise PasswordNotMatch

        validate_password(data['password'])
        return data

    def save(self):
        password = self.validated_data['password']
        email = self.validated_data['email']

        account = CustomUser(email=email)
        account.set_password(password)
        account.save()
        return account
    

class EmailLogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

        
