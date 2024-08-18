from django.urls import include, path
from .views import *


app_name = "metadata"

urlpatterns = [
    path("api/", include("apps.metadata.api.urls"), name="api"),
]
