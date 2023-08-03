from django.contrib.auth.forms import UserCreationForm
from .models import User, File
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def validate_allowed_file(value):
    extension = value.name.split(".")[-1]
    allowed_extensions = ["pdf", "jpg", "jpeg", "png", "mp3", "mp4", "mkv"]
    if extension.lower() not in allowed_extensions:
        raise forms.ValidationError("Unsupported file type")


class FileAdminForm(forms.ModelForm):
    class Meta:
        model = File
        fields = "__all__"

    file = forms.FileField(validators=[validate_allowed_file])
