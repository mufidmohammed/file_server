from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import File, User


# Register your models here.
class FileAdmin(admin.ModelAdmin):
    fields = [
        "title", "description", "file"
    ]

    list_display = ["title", "previews", "emails_sent"]


admin.site.register(User, UserAdmin)
admin.site.register(File, FileAdmin)
