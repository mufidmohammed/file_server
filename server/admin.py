from django.contrib import admin
from .models import File
from .forms import FileAdminForm


# Register your models here.
class FileAdmin(admin.ModelAdmin):
    form = FileAdminForm
    
    fields = [
        "title", "description", "file"
    ]

    list_display = ["title", "downloads", "emails_sent"]


admin.site.register(File, FileAdmin)
