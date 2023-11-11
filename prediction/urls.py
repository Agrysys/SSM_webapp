from django.urls import path

from . import views

app_name = "prediction"
urlpatterns = [
    path("image", views.index, name="index"),
    path("coba", views.coba),
    path("upload", views.upload, name="upload")
]