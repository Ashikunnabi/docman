from django.urls import include, path


app_name = "api"

urlpatterns = [
    path("v1/auth/", include("apps.authentication.api.v1.urls")),
]
