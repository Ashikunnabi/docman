from django.urls import path

from .viewsets import (
    CategoryGroupPermissionDeleteAPIView,
    CategoryGroupPermissionListCreateAPIView,
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
    path(
        "<uuid:uuid>/groups/",
        CategoryGroupPermissionListCreateAPIView.as_view(),
        name="category_group_permission_list_create",
    ),
    path(
        "<uuid:uuid>/groups/<int:group_id>/category-group-permission/<uuid:category_group_permission_uuid>/",
        CategoryGroupPermissionDeleteAPIView.as_view(),
        name="category_group_permission_delete",
    ),
]
