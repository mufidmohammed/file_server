from django.shortcuts import render

from .models import File


# Create your views here.
def index(request):
    if request.method == "POST":
        search = request.POST["search"]
        files = File.objects.filter(title__contains=search)
    else:
        files = File.objects.all()
    return render(request, "server/feed.html", {"files": files})
