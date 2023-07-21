from django.core.mail import EmailMessage
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


def create_email(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    # get message after email sent successfully
    message = request.GET.get("message", None)
    return render(request, "server/email.html", {"file": file, "message": message})


def send_email(request):
    file_id = request.POST['id']
    file_object = get_object_or_404(File, pk=file_id)

    subject = file_object.title
    message = file_object.description
    # replace by request.user.email
    # after client authentication is done
    sender = "user@email.com"
    receiver = [request.POST['receiver']]

    email = EmailMessage(subject, message, sender, receiver)
    email.content_subtype = 'html'

    file = file_object.file

    email.attach_file(file.path)
    email.send()

    # increment emails_sent for the file model
    file_object.emails_sent += 1
    file_object.save()

    message = 'File emailed successfully'
    return redirect(f"{request.META['HTTP_REFERER']}?message={message}")


