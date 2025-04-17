from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user_auth_app.models import CustomUser
from movie_app.models import Movie, UserMovieProgress


class MovieProgressSlugTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        
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
        cls.movie_progress = UserMovieProgress.objects.create(
            user=cls.user,
            movie=cls.movie,
            progress_seconds=0,
            finished=False,
        )
        cls.url = reverse('movie-progress-detail', kwargs={'slug': cls.movie.slug})

    def test_get_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['movie']['id'], self.movie.id)
        self.assertEqual(response.data['progress_seconds'], 0)
        self.assertFalse(response.data['finished'])

    def test_get_authenticated_no_progress(self):
        url = reverse('movie-progress-detail', kwargs={'slug': 'non-existent-movie'})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No object with this slug.')

    def test_patch_unauthenticated(self):
        response = self.client.patch(self.url, data={'progress_seconds': 60}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_patch_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data={'progress_seconds': 60}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie_progress.refresh_from_db()
        self.assertEqual(self.movie_progress.progress_seconds, 60)
    
    def test_patch_authenticated_no_progress(self):
        url = reverse('movie-progress-detail', kwargs={'slug': 'non-existent-movie'})
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data={'progress_seconds': 60}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No object with this slug.')

    def test_patch_authenticated_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data={'progress_seconds': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('progress_seconds', response.data)

    