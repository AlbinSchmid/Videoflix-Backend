from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from movie_app.models import Movie, UserMovieProgress
from .serializer import MovieSerializer, UserMovieProgressSerializer
from .exeptions import NoObjectWithThisSug
from user_auth_app.api.permissions import IsLoggedIn
from .utils import get_serialized_movies


class UserMovieProgressDetailView(generics.RetrieveUpdateAPIView):
    """View to handle user movie progress detail."""
    permission_classes = [IsLoggedIn]
    serializer_class = UserMovieProgressSerializer
    lookup_field = 'slug'
    queryset = UserMovieProgress.objects.all()

    def get(self, request, *args, **kwargs):
        """Get user movie progress by slug."""
        user_movie_progress = UserMovieProgress.objects.filter(
            user=request.user, movie__slug=kwargs['slug']).first()
        if user_movie_progress:
            serializer = UserMovieProgressSerializer(
                user_movie_progress, context={'request': request})
            return Response(serializer.data, status=200)
        raise NoObjectWithThisSug

    def patch(self, request, *args, **kwargs):
        """Update user movie progress by slug."""
        user_movie_progress = UserMovieProgress.objects.filter(
            user=request.user, movie__slug=kwargs['slug']).first()
        if user_movie_progress:
            serializer = UserMovieProgressSerializer(
                user_movie_progress,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        raise NoObjectWithThisSug


class UserMovieProgressListView(generics.ListCreateAPIView):
    """View to handle user movie progress list."""
    permission_classes = [IsLoggedIn]
    serializer_class = UserMovieProgressSerializer
    queryset = UserMovieProgress.objects.all()

    def perform_create(self, serializer):
        """Create user movie progress."""
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """Get user movie progress list."""
        user_movie_progress = UserMovieProgress.objects.filter(
            user=request.user).order_by('-updated_at')
        if user_movie_progress.exists():
            serializer = UserMovieProgressSerializer(
                user_movie_progress, many=True, context={'request': request})
            return Response(serializer.data, status=200)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieListView(generics.ListAPIView):
    """View to handle movie list."""
    permission_classes = [IsLoggedIn]
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def get(self, request, *args, **kwargs):
        """Get movie list with categories."""
        categories = [
            'Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Family', 'Fantasy', 'History',
            'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction',
            'Sport', 'Thriller', 'War', 'Western',
        ]
        data = {}
        context = {'request': request}
        date_treshold = timezone.now() - timedelta(days=14)

        data['new_on_videoflix'] = get_serialized_movies(Movie.objects.filter(created_at__gte=date_treshold), MovieSerializer, '-created_at',  context)
        data['continue_watching'] = get_serialized_movies(UserMovieProgress.objects.filter(user=request.user, finished=False), UserMovieProgressSerializer, '-updated_at', context)
        data['watched'] = get_serialized_movies(UserMovieProgress.objects.filter(user=request.user, finished=True), UserMovieProgressSerializer, '-updated_at', context)

        for category in categories:
            data[category.lower()] = get_serialized_movies(Movie.objects.filter(
                category__iexact=category), MovieSerializer, '-created_at', context)

        return Response(data)
