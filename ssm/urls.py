from django.urls import path, include

from . import views

app_name = "ssm"
api_Patern = [
    path("predict/class",views.predict, name="get class"),
]

urlpatterns = [
    path("image", views.index, name="index"),
    path("coba", views.coba),
    path("api/v1/",include(api_Patern)),
    path("melon", views.data_melons, name="data.melon"),
    path("dashboard", views.dashboard, name="dashboard")
]

