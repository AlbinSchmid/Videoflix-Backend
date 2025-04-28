from django.contrib import admin
from .models import CustomUser
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class UserResource(resources.ModelResource):
    """Resource class for importing and exporting CustomUser data."""
    class Meta:
        """Meta class to define the model and fields to be imported/exported."""
        model = CustomUser 

@admin.register(CustomUser)
class UserAdmin(ImportExportModelAdmin):
    """Admin class for CustomUser model."""
    pass
