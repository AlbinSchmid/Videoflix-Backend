from rest_framework import serializers
from movie_app.models import Movie, UserMovieProgress


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model."""
    hls_url = serializers.SerializerMethodField()
    movie_cover = serializers.SerializerMethodField()
    movie_cover_phone = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'slug', 'description', 'category', 'movie_cover', 'movie_cover_phone',
                  'hls_url', 'author', 'author_url', 'license', 'license_url', 'release_year']

    def get_hls_url(self, obj):
        """Get the HLS URL for the movie."""
        request = self.context.get('request')
        return request.build_absolute_uri(f'/media/movies/{obj.slug}/{obj.slug}.m3u8') #.replace('http://', 'https://')
    
    def get_movie_cover(self, obj):
        """Get the movie cover URL."""
        request = self.context.get('request')
        return request.build_absolute_uri(obj.movie_cover.url) #.replace('http://', 'https://')

    def get_movie_cover_phone(self, obj):
        """Get the movie cover URL for phone."""
        request = self.context.get('request')
        return request.build_absolute_uri(obj.movie_cover_phone.url) #.replace('http://', 'https://')


class UserMovieProgressSerializer(serializers.ModelSerializer):
    """Serializer for UserMovieProgress model."""
    movie = MovieSerializer(read_only=True)
    movie_slug = serializers.SlugRelatedField(
        queryset=Movie.objects.all(),
        slug_field='slug',
        write_only=True,
        source='movie'
    )

    class Meta:
        """Meta class for UserMovieProgressSerializer."""
        model = UserMovieProgress
        fields = '__all__'
        read_only_fields = ['user', 'updated_at', 'movie']
