from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from movie_app.models import Movie, UserMovieProgress
from .serializer import MovieSerializer, UserMovieProgressSerializer
from .exeptions import NoObjectWithThisSug
from user_auth_app.api.permissions import IsLoggedIn

class UserMovieProgressDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsLoggedIn]
    serializer_class = UserMovieProgressSerializer
    lookup_field = 'slug'
    queryset = UserMovieProgress.objects.all()

    def get(self, request, *args, **kwargs):
        user_movie_progress = UserMovieProgress.objects.filter(
            user=request.user, movie__slug=kwargs['slug']).first()
        if user_movie_progress:
            serializer = UserMovieProgressSerializer(
                user_movie_progress, context={'request': request})
            return Response(serializer.data, status=200)
        raise NoObjectWithThisSug
    
    def patch(self, request, *args, **kwargs):
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
    permission_classes = [IsLoggedIn]
    serializer_class = UserMovieProgressSerializer
    queryset = UserMovieProgress.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        user_movie_progress = UserMovieProgress.objects.filter(
            user=request.user).order_by('-updated_at')
        if user_movie_progress.exists():
            serializer = UserMovieProgressSerializer(
                user_movie_progress, many=True, context={'request': request})
            return Response(serializer.data, status=200)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieListView(generics.ListAPIView):
    permission_classes = [IsLoggedIn]
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def get(self, request, *args, **kwargs):
        categories = [
            'Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Family', 'Fantasy', 'History',
            'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction',
            'Sport', 'Thriller', 'War', 'Western'
        ]
        data = {}
        context = {'request': request}

        date_treshold = timezone.now() - timedelta(days=14)
        movies = Movie.objects.filter(created_at__gte=date_treshold)[:10]
        serializer = MovieSerializer(movies, many=True, context=context)
        data['new_on_videoflix'] = serializer.data

        for category in categories:
            movies = Movie.objects.filter(category__iexact=category)[:10]
            serializer = MovieSerializer(movies, many=True, context=context)
            data[category.lower()] = serializer.data

        movie = UserMovieProgress.objects.filter(
            user=request.user, finished=False).order_by('-updated_at')[:10]
        serializer = UserMovieProgressSerializer(
            movie, many=True, context=context)
        data['continue_watching'] = serializer.data

        movie = UserMovieProgress.objects.filter(
            user=request.user, finished=True).order_by('-updated_at')[:10]
        serializer = UserMovieProgressSerializer(
            movie, many=True, context=context)
        data['watched'] = serializer.data

        return Response(data)
