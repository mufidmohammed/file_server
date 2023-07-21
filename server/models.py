from django.db import models


# Create your models here.
class File(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    file = models.FileField()
    previews = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
