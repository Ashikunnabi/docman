from django.urls import include, path


app_name = "search"

urlpatterns = [
    path("api/", include("apps.search.api.urls"), name="api"),
]
