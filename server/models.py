from django.contrib.auth.models import User
from django.db import models

User._meta.get_field('email')._unique = True


class File(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    file = models.FileField()
    previews = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
