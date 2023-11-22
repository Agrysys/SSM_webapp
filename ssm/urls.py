from django.urls import path, include

from . import views

app_name = "ssm"
api_Patern = [
    path("predict/class",views.predict, name="get class"),
    path("glcm/<str:pk>",views.get_glcm, name= "get_glcm"),
    path("predict",views.predict2, name="prediction")
]

urlpatterns = [
    path("image", views.index, name="index"),
    path("coba", views.coba),
    path("api/v1/",include(api_Patern)),
    path("melon", views.data_melons, name="data.melon"),
    path("dashboard", views.dashboard, name="dashboard")
]

