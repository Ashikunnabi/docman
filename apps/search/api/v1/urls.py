from django.urls import path

from .viewsets import (
    DocumentSearchAPIView,
)


app_name = "v1"

urlpatterns = [
    path("documents/", DocumentSearchAPIView.as_view(), name="search_document_list"),
]
