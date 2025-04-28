from django.apps import AppConfig


class UserAuthAppConfig(AppConfig):
    """Configuration class for the user authentication app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_auth_app'

    def ready(self):
        """Override the ready method to import signals."""
        import user_auth_app.api.signals
