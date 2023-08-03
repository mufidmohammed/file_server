from django.contrib.auth import views as auth_view
from django.urls import path

from . import views

app_name = "server"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:file_id>/download/", views.download, name="download"),
    path("<int:file_id>/email/", views.create_email, name="create_email"),
    path("email/", views.send_email, name="send_email"),
    path("register/", views.register, name='register'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout")
]
