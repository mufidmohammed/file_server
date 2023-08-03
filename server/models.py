from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]


class File(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    file = models.FileField()
    downloads = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
