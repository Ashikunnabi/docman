from django.urls import include, path
from .views import *


app_name = "menu"

urlpatterns = [
    path("api/", include("apps.menu.dashboard_api.urls"), name="dashboard_api"),
    path("api/", include("apps.menu.api.urls"), name="api"),
]
