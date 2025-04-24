from django.contrib import admin
from .models import Movie, UserMovieProgress
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MovieResource(resources.ModelResource):

    class Meta:
        model = Movie  # or 'core.Book'

class MovieProgressResource(resources.ModelResource):

    class Meta:
        model = UserMovieProgress  # or 'core.Book'

@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    exclude = ('slug',) 

@admin.register(UserMovieProgress)
class MovieProgressAdmin(ImportExportModelAdmin):
    pass
