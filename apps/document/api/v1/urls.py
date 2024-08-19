from django.urls import path

from .viewsets import (
    DocumentListCreateAPIView,
    DocumentRetrieveUpdateDestroyAPIView,
    DocumentMetadataValueUpdateAPIView,
)


app_name = "v1"

urlpatterns = [
    path("", DocumentListCreateAPIView.as_view(), name="document_list_create"),
    path("<uuid:uuid>/", DocumentRetrieveUpdateDestroyAPIView.as_view(), name="document_retrieve_update_destroy"),
    path("<uuid:uuid>/metadata-values/", DocumentMetadataValueUpdateAPIView.as_view(), name="document_metadata_values_update"),
]
