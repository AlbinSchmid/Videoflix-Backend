from django.contrib import admin
from .models import Movie

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    exclude = ('slug',) 

admin.site.register(Movie, MovieAdmin)
