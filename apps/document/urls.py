from django.urls import include, path


app_name = "document"

urlpatterns = [
    path("api/", include("apps.document.api.urls"), name="api"),
]
