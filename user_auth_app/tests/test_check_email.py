from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser

class CheckEmailTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('check-email')
        cls.user = CustomUser.objects.create_user(email='test@gmail.com', password='testPassword123')
        cls.data = {
            'email': 'test@gmail.com'
        }

    def test_post_email_exist(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exist'])

    def test_post_email_not_exist(self):
        self.data['email'] = 'change@gmail.com'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['exist'])