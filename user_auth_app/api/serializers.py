from rest_framework import serializers
from user_auth_app.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from .exeptions import PasswordNotMatch, EmailExistAlready

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    repeated_password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise EmailExistAlready

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
