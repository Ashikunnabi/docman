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
                path(
                    "<uuid:metadata_uuid>/fields/add/",
                    metadata_field_add,
                    name="metadata_field_add",
                ),
                path(
                    "<uuid:metadata_uuid>/fields/edit/<uuid:uuid>/",
                    metadata_field_edit,
                    name="metadata_field_edit",
                ),
            ]
        ),
    ),
]
