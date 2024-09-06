from django.urls import path

from .viewsets import (
    DocumentListCreateAPIView,
    DocumentRetrieveUpdateDestroyAPIView,
    DocumentMetadataValueUpdateAPIView,
    DocumentSearchAPIView,
    DocumentUploadAPIView,
)


app_name = "v1"

urlpatterns = [
    path("", DocumentListCreateAPIView.as_view(), name="document_list_create"),
    path("<uuid:uuid>/", DocumentRetrieveUpdateDestroyAPIView.as_view(), name="document_retrieve_update_destroy"),
    path("<uuid:uuid>/metadata/", DocumentMetadataValueUpdateAPIView.as_view(), name="document_metadata_values_update"),
    path("search/", DocumentSearchAPIView.as_view(), name="document_search"),
    path("upload/", DocumentUploadAPIView.as_view(), name="document_upload"),
]
