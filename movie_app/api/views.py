from rest_framework import generics
from movie_app.models import Movie
from .serializer import MovieSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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

        for category in categories:
            movies = Movie.objects.filter(category__iexact=category)[:10]
            data[category.lower()] = MovieSerializer(movies, many=True).data


        return Response(data)
