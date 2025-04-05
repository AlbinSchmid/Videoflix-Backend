from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser


class ForgotPasswordTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('forgot-password')
        cls.user = CustomUser.objects.create_user(email='test@gmail.com', password='testPassword123', is_active=True)
        cls.data = {
            'email': cls.user.email,
        }

    def test_post_success(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('We have sent you an email with instructions to reset your password.', response.data['message'])

    def test_post_not_verified(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Please verify your account before reset your password.', response.data['detail'])

    def test_post_user_not_found(self):
        self.data['email'] = 'notFound'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User with this email was not found.', response.data['detail'])




