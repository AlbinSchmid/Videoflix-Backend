from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class ResetPasswordTests(APITestCase):
    """Test case for the reset password view."""
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the test case."""
        cls.url = reverse('reset-password')
        cls.user = CustomUser.objects.create_user(email='test@gmail.com', password='testPassword123', is_active=True)
        uid = urlsafe_base64_encode(force_bytes(cls.user.pk))
        token = default_token_generator.make_token(cls.user)
        cls.data = {
            'uid': uid,
            'token': token,
            'password': 'newPassword123',
            'repeated_password': 'newPassword123'
        }

    def test_post_success(self):
        """Test the reset password view with valid uid and token."""
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Your password was reset successfully. You can now log in with your new password.', response.data['detail'])
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newPassword123'))
    
    def test_post_not_verified(self):
        """Test the reset password view with a non-verified email."""
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Please verify your account before reset your password.', response.data['detail'])

    def test_post_incorrect_url(self):
        """Test the reset password view with an incorrect URL."""
        self.data['uid'] = 'incorrect_uid'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('The link you used is invalid or no longer active.', response.data['detail'])

    def test_post_incorrect_token(self):
        """Test the reset password view with an incorrect token."""
        self.data['token'] = 'incorrect_token'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('The link you used is invalid or no longer active.', response.data['detail'])

    def test_post_password_not_match(self):
        """Test the reset password view with non-matching passwords."""
        self.data['repeated_password'] = 'differentPassword123'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords not match.', response.data['detail'])

    def test_post_password_same_as_old(self):
        """Test the reset password view with the same password."""
        self.data['password'] = 'testPassword123'
        self.data['repeated_password'] = 'testPassword123'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('New password cannot be the same as the old one.', response.data['detail'])

    def test_post_password_too_short(self):
        """Test the reset password view with a password that is too short."""
        self.data['password'] = 'short'
        self.data['repeated_password'] = 'short'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This password is too short. It must contain at least 8 characters.', response.data['password'][0])