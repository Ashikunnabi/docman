from django.urls import path

from .viewsets import (
    DocumentListCreateAPIView,
    DocumentRetrieveUpdateDestroyAPIView,
)


app_name = "v1"

urlpatterns = [
    path("", DocumentListCreateAPIView.as_view(), name="document_list_create"),
    path("<uuid:uuid>/", DocumentRetrieveUpdateDestroyAPIView.as_view(), name="document_retrieve_update_destroy"),
]
