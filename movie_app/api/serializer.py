from rest_framework import serializers
from movie_app.models import Movie, UserMovieProgress

class MovieSerializer(serializers.ModelSerializer):
    hls_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'slug', 'description', 'category', 'movie_cover', 'movie_cover_phone', 'hls_url', 'author', 'author_url', 'license', 'license_url', 'release_year']

    def get_hls_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/media/movies/{obj.slug}/{obj.slug}.m3u8')
    

class UserMovieProgressSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        write_only=True,
        source='movie'
    ) 

    class Meta:
        model = UserMovieProgress
        fields = '__all__'
        read_only_fields = ['user', 'updated_at', 'movie']
