from django.contrib import admin
from .models import Movie, UserMovieProgress
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MovieResource(resources.ModelResource):
    """Resource class for Movie model."""
    class Meta:
        """Meta class for MovieResource."""
        model = Movie

class MovieProgressResource(resources.ModelResource):
    """Resource class for UserMovieProgress model."""
    class Meta:
        """Meta class for MovieProgressResource."""
        model = UserMovieProgress

@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    """Admin class for Movie model."""
    exclude = ('slug',) 

@admin.register(UserMovieProgress)
class MovieProgressAdmin(ImportExportModelAdmin):
    """Admin class for UserMovieProgress model."""
    pass
