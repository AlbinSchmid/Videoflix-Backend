from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser
from movie_app.models import Movie, UserMovieProgress


class MovieProgressTest(APITestCase):
    """Test case for movie progress API."""
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the test case."""
        cls.url = reverse('movie-progress')
        cls.user = CustomUser.objects.create_user(
            email='test@gmail.com', password='testPassword123')
        cls.movie = Movie.objects.create(
            title='Test Movie',
            slug='test-movie',
            description='Test Description',
            release_year=2023,
            category='Action',
            video_file='test_video.mp4',
            movie_cover_phone='test_cover_phone.jpg',
            movie_cover='test_cover.jpg',
        )
        cls.data = {
            'movie_slug': cls.movie.slug,
        }

    def test_getunauthenticated(self):
        """Test GET request without authentication."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Log in to your account to continue.')

    def test_get_authenticated_not_exist(self):
        """Test GET request with authentication but no progress."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_authenticated_exist(self):
        """Test GET request with authentication and existing progress."""
        UserMovieProgress.objects.create(
            user=self.user,
            movie=self.movie,
            progress_seconds=120,
            finished=False,
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)
        self.assertEqual(response.data[0]['progress_seconds'], 120)
        self.assertEqual(response.data[0]['movie']['id'], self.movie.id)
        self.assertFalse(response.data[0]['finished'], False)

    def test_post_unauthenticated(self):
        """Test POST request without authentication."""
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Log in to your account to continue.')

    def test_post_authenticated(self):
        """Test POST request with authentication."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['progress_seconds'], 0)
        self.assertEqual(response.data['movie']['id'], self.movie.id)
        self.assertFalse(response.data['finished'], False)

    def test_post_authenticated_incorrect_slug(self):
        """Test POST request with authentication and incorrect movie slug."""
        self.client.force_authenticate(user=self.user)
        self.data['movie_slug'] = 'incorrect-slug'
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)