from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_auth_app.models import CustomUser
from .serializers import RegistrationSerializer


class LoginView(generics.ListAPIView):
    pass


class RegistrationView(APIView):
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            data = {
                'token': token.key,
                'id': user.id
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
