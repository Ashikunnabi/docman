from django.urls import include, path
from .views import *


app_name = "admin_metadata"

urlpatterns = [
    path(
        "metadata/",
        include(
            [
                path("", metadata_list, name="metadata_list"),
                path("add/", metadata_add, name="metadata_add"),
                path("edit/<uuid:uuid>/", metadata_edit, name="metadata_edit"),
            ]
        ),
    ),
]
