from django.urls import path

from .viewsets import (
    MetadataListCreateAPIView,
    MetadataRetrieveUpdateDestroyAPIView,
)

app_name = "v1"

urlpatterns = [
    path(
        "",
        MetadataListCreateAPIView.as_view(),
        name="metadata_list_create",
    ),
    path(
        "<uuid:uuid>/",
        MetadataRetrieveUpdateDestroyAPIView.as_view(),
        name="metadata_retrieve_update_delete",
    ),
]
