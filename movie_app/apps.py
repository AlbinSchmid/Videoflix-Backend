from django.apps import AppConfig


class MovieAppConfig(AppConfig):
    """Configuration class for the movie app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie_app'

    def ready(self):
        """Override the ready method to import signals."""
        import movie_app.api.signals
