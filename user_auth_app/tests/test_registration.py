from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser

class RegistrationTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('registration')
        cls.data = {
            'email': 'test@gmail.com',
            'password': 'testPassword123',
            'repeated_password': 'testPassword123'
        }

    def test_post_success(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_password_not_match(self):
        self.data['repeated_password'] = 'differentPassword123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords not match', response.data['detail'])

    def test_post_email_exist_already(self):
        CustomUser.objects.create_user(
            email=self.data['email'],
            password=self.data['password']
        )
        self.client.post(self.url, self.data, format='json')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('An account with this email already exists', response.data['detail'])

    def test_post_invalid_email(self):
        self.data['email'] = 'invalidEmail'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address', response.data['email'][0])

    def test_post_empty_email(self):
        self.data['email'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank', response.data['email'][0])

    def test_post_empty_password(self):
        self.data['password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank', response.data['password'][0])

    def test_post_empty_repeated_password(self):
        self.data['repeated_password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank', response.data['repeated_password'][0])
