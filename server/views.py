from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect

from .models import File, User

from .forms import CreateUserForm


@login_required
def index(request):
    if request.method == "POST":
        search = request.POST["search"]
        files = File.objects.filter(title__contains=search)
    else:
        files = File.objects.all()
    return render(request, "server/feed.html", {"files": files})

@login_required
def preview(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.previews += 1
    file.save()
    return redirect(file.file.url)

@login_required
def create_email(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    # get message after email sent successfully
    message = request.GET.get("message", None)
    return render(request, "server/email.html", {"file": file, "message": message})

@login_required
def send_email(request):
    file_id = request.POST["id"]
    file_object = get_object_or_404(File, pk=file_id)

    subject = file_object.title
    message = file_object.description

    sender = request.user.email
    receiver = [request.POST["receiver"]]

    email = EmailMessage(subject, message, sender, receiver)
    email.content_subtype = "html"

    file = file_object.file

    email.attach_file(file.path)
    email.send()

    # increment emails_sent for the file model
    file_object.emails_sent += 1
    file_object.save()

    message = "File emailed successfully"
    return redirect(f"{request.META['HTTP_REFERER']}?message={message}")


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("server:login")
    else:
        form = CreateUserForm()

    return render(request, "server/auth/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect("server:index")
        message = "Email and password do not match any user. Please try again"
    else:
        message = ""

    return render(request, "server/auth/login.html", {"message": message})
