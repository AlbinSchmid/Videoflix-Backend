from rest_framework import generics
from movie_app.models import Movie, UserMovieProgress
from .serializer import MovieSerializer, UserMovieProgressSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta

class UserMovieProgressView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserMovieProgressSerializer
    queryset = UserMovieProgress.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MovieListView(generics.ListAPIView):
    permission_classes = [AllowAny]
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

        for category in categories:
            movies = Movie.objects.filter(category__iexact=category)[:10]
            serializer = MovieSerializer(movies, many=True, context=context)
            data[category.lower()] = serializer.data

        date_treshold = timezone.now() - timedelta(days=14)
        movies = Movie.objects.filter(created_at__gte=date_treshold)[:10]
        serializer = MovieSerializer(movies, many=True, context=context)
        data['new_on_videoflix'] = serializer.data

        return Response(data)


class MovieBySlugView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = MovieSerializer
    lookup_field = 'slug'
    queryset = Movie.objects.all()
