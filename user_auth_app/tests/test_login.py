from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser

class LoginTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('login')
        cls.user = CustomUser.objects.create_user(email='test@gmail.com', password='testPassword123')
        cls.data = {
            'email': 'test@gmail.com',
            'password': 'testPassword123'
        }

    def test_post_success(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.post(self.url, self.data, format='json')
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_correct_data_not_verified(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Please verify your account before logging in.', response.data['detail'])

    def test_post_incorrect_email(self):
        self.data['email'] = 'invalidEmail' 
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address.', response.data['email'])

    def test_post_email_not_exist(self):
        self.data['email'] = 'not@gmail.com' 
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid email or password.', response.data['detail'])

    def test_post_incorrect_password(self):
        self.data['password'] = 'wrongPassword123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid email or password.', response.data['detail'])

    def test_post_empty_email(self):
        self.data['email'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['email'])

    def test_post_empty_password(self):
        self.data['password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.data['password'])