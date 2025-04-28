from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class ActivateTests(APITestCase):
    """Test case for the account activation view."""
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the test case."""
        cls.url = reverse('activate')
        cls.user = CustomUser.objects.create_user(email='test@gmail.com', password='testPassword123', is_active=False)
        uid = urlsafe_base64_encode(force_bytes(cls.user.pk))
        token = default_token_generator.make_token(cls.user)
        cls.data = {
            'uid': uid,
            'token': token
        }

    def test_post_success(self):
        """Test the account activation with valid uid and token."""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertIn('Your account has been successfully verified. You can now log in and start using Videoflix.', response.data['message'])

    def test_post_invalid_uid(self):
        """Test the account activation with an invalid uid."""
        self.data['uid'] = 'invalidUid'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('The link you used is invalid or no longer active.', response.data['detail'])
