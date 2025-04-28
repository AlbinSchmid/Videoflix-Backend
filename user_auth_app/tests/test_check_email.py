from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser

class CheckEmailTests(APITestCase):
    """Test case for the check email view."""
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the test case."""
        cls.url = reverse('check-email')
        cls.user = CustomUser.objects.create_user(email='test@gmail.com', password='testPassword123')
        cls.data = {
            'email': 'test@gmail.com'
        }

    def test_post_email_exist(self):
        """Test the check email view with an existing email."""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exist'])

    def test_post_email_not_exist(self):
        """Test the check email view with a non-existing email."""
        self.data['email'] = 'change@gmail.com'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['exist'])