from django.urls import path, include

from . import views

app_name = "ssm"
api_Patern = [
    path("predict/class",views.predict, name="get class"),
    path('glcm/<str:kode>',views.get_glcm, name='get glcm'),
    path('melon/lastweek',views.get_count_in_a_week, name='lastweek')
]

urlpatterns = [
    path("api/v1/",include(api_Patern)),
    path("melon", views.data_melons, name="data.melon"),
    path("test-melon", views.data_melon_test, name="Melon-test"),
    path("dashboard", views.dashboard, name="dashboard")
]

