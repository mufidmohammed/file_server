import os

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import FileResponse
from django.template.loader import get_template

from .models import File

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
def download(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    
    file.downloads += 1
    file.save()
    
    file_path = file.file.path

    file_name = os.path.basename(file_path)

    response = FileResponse(open(file_path, "rb"), content_type="application/octet-stream")
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    file.downloads += 1
    file.save()

    return response


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
    try:
        email.send()
        # increment emails_sent for the file model
        file_object.emails_sent += 1
        file_object.save()
        message = "File emailed successfully"
    except ConnectionRefusedError:
        message = "File emailing not configured to work in production. Please test locally"

    return redirect(f"{request.META['HTTP_REFERER']}?message={message}")


def send_confirmation_email(username, subject, to_email, data):
    from_email = "test@email.com"
    htmly = get_template("server/auth/confirmation_email.html")
    html_content = htmly.render(data)
    email = EmailMessage(subject, html_content, from_email, to_email)
    email.content_subtype = "html"
    try:
        email.send()
    except ConnectionRefusedError:
        pass    # production environment
        


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            # send confirmation email upon signup
            username = form.cleaned_data.get("username")
            email = [form.cleaned_data.get("email")]
            data = {
                "title": "Signup successful", 
                "message": f"Congratulations {username}. Your account has been created successfully"
            }

            send_confirmation_email(username, "account creation", email, data)

            return redirect("server:login")
    else:
        form = CreateUserForm()

    return render(request, "server/auth/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        email = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            
            # send confirmation email after login
            username = user.username
            to_email = [email]

            data = {
                "title": "Account Login",
                "message": f"Hello {username}, Your account has been logged in recently. If it was not you, kindly reset your password"
            }

            send_confirmation_email(username, "account login", to_email, data)

            return redirect("server:index")
        
        message = "Email and password do not match any user. Please try again"
        form = AuthenticationForm(request.POST)
    else:
        message = ""
        form = AuthenticationForm()

    return render(request, "server/auth/login.html", {"message": message, "form": form})


def user_logout(request):
    logout(request)
    return redirect("server:login")
