from rest_framework import serializers
from movie_app.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    movie_cover = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_movie_cover(self, obj):
        request = self.context.get('request')
        if obj.movie_cover and request:
            return request.build_absolute_uri(obj.movie_cover.url)
        return None