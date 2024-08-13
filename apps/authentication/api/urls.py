from django.urls import include, path


app_name = "api"

urlpatterns = [
    path("v1/", include("apps.authentication.api.v1.urls")),
]
