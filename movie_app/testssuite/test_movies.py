from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from user_auth_app.models import CustomUser
from django.conf import settings


class MovieTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('movies')
        cls.user = CustomUser.objects.create_user(
            email='test@gmail.com', password='testPassword123')

    def test_get_movies_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['detail'], 'Log in to your account to continue.')

    def test_get_movies_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
