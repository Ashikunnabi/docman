from django.urls import include, path


app_name = "api"

urlpatterns = [
    path("v1/documents/", include("apps.document.api.v1.urls")),
]
