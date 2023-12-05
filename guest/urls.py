from django.urls import path, include

from . import views
app_name = "guest"

RestApiPatter = [
    path("predict-test",views.predict_test, name="predict_test"),
]

urlpatterns = [
    path("pred", views.melon_test_view, name="prediction"),
    path("",views.landing, name="landing"),
    path("api/v1/",include(RestApiPatter))
]
