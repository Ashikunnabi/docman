from django.urls import include, path


app_name = "api"

urlpatterns = [
    path("v1/search/", include("apps.search.api.v1.urls")),
]
