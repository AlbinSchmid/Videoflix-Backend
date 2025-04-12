from rest_framework import serializers
from movie_app.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    hls_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'category', 'movie_cover', 'movie_cover_phone', 'hls_url']

    def get_hls_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/media/movies/{obj.slug}/master.m3u8')
