from django.urls import path

from .viewsets import (
    MetadataListCreateAPIView,
    MetadataRetrieveUpdateDestroyAPIView,
    MetadataFieldListCreateAPIView,
    MetadataFieldRetrieveUpdateDestroyAPIView,
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
    path(
        "<uuid:uuid>/fields/",
        MetadataFieldListCreateAPIView.as_view(),
        name="metadata_field_list_create",
    ),
    path(
        "<uuid:uuid>/fields/<uuid:field_uuid>/",
        MetadataFieldRetrieveUpdateDestroyAPIView.as_view(),
        name="metadata_field_retrieve_update_delete",
    ),
]
