from django.contrib import admin
from .models import CustomUser
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class UserResource(resources.ModelResource):

    class Meta:
        model = CustomUser 

@admin.register(CustomUser)
class UserAdmin(ImportExportModelAdmin):
    pass
