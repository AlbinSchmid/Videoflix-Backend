from rest_framework import generics
from movie_app.models import Movie
from .serializer import MovieSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import caches


class MovieListView(generics.ListAPIView):
    print(f"Aktiver Cache-Backend: {type(caches['default'])}")
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
        return Response(data)
