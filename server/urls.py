from django.urls import path

from . import views

app_name = "server"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:file_id>/preview/", views.preview, name="preview"),
    path("<int:file_id>/email/", views.create_email, name="create_email"),
    path('email/', views.send_email, name='send_email'),

]
