from django.shortcuts import render

from .models import File


# Create your views here.
def index(request):
    files = File.objects.all()
    return render(request, "server/feed.html", {"files": files})
