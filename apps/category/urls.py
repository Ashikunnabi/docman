from django.urls import include, path
from .views import *


app_name = "category"

urlpatterns = [
    path("api/", include("apps.category.api.urls"), name="api"),
]
