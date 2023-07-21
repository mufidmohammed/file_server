from django.shortcuts import render, get_object_or_404, redirect

from .models import File


# Create your views here.
def index(request):
    if request.method == "POST":
        search = request.POST["search"]
        files = File.objects.filter(title__contains=search)
    else:
        files = File.objects.all()
    return render(request, "server/feed.html", {"files": files})


def preview(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.previews += 1
    file.save()
    return redirect(file.file.url)
