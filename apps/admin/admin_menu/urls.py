from django.urls import include, path

from .views import *

app_name = "admin_menu"

urlpatterns = [
    path(
        "menu-types/",
        include(
            [
                path("", menu_type_list, name="menu_type_list"),
                path("add/", menu_type_add, name="menu_type_add"),
                path("edit/<str:uuid>/", menu_type_edit, name="menu_type_edit"),
            ]
        ),
    ),
    path(
        "menus/",
        include(
            [
                path("", menu_list, name="menu_list"),
                path("add/", menu_add, name="menu_add"),
                path("edit/<str:uuid>/", menu_edit, name="menu_edit"),
            ]
        ),
    ),
]
