from django.urls import path

from .viewsets import (
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
)

app_name = "v1"

urlpatterns = [
    path(
        "",
        CategoryListCreateAPIView.as_view(),
        name="category_list_create",
    ),
    path(
        "<uuid:uuid>/",
        CategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="category_retrieve_update_delete",
    ),
]
