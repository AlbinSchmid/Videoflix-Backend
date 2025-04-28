from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser

class RegistrationTests(APITestCase):
    """Test case for the registration view."""
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the test case."""
        cls.url = reverse('registration')
        cls.data = {
            'email': 'test@gmail.com',
            'password': 'testPassword123',
            'repeated_password': 'testPassword123'
        }

    def test_post_success(self):
        """Test the registration view with valid data."""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_password_not_match(self):
        """Test the registration view with non-matching passwords."""
        self.data['repeated_password'] = 'differentPassword123'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords not match', response.data['detail'])

    def test_post_email_exist_already(self):
        """Test the registration view with an existing email."""
        CustomUser.objects.create_user(
            email=self.data['email'],
            password=self.data['password']
        )
        self.client.post(self.url, self.data, format='json')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('An account with this email already exists', response.data['detail'])

    def test_post_invalid_email(self):
        """Test the registration view with an invalid email."""
        self.data['email'] = 'invalidEmail'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid email address', response.data['email'][0])

    def test_post_empty_email(self):
        """Test the registration view with an empty email."""
        self.data['email'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank', response.data['email'][0])

    def test_post_empty_password(self):
        """Test the registration view with an empty password."""
        self.data['password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank', response.data['password'][0])

    def test_post_empty_repeated_password(self):
        """Test the registration view with an empty repeated password."""
        self.data['repeated_password'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank', response.data['repeated_password'][0])
