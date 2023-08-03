from django.contrib import admin
from .models import File


# Register your models here.
class FileAdmin(admin.ModelAdmin):
    fields = [
        "title", "description", "file"
    ]

    list_display = ["title", "downloads", "emails_sent"]


admin.site.register(File, FileAdmin)
