from django.urls import include, path
from .views import *


app_name = "admin_category"

urlpatterns = [
    path(
        "category/",
        include(
            [
                path("edit/<uuid:uuid>/", category_edit, name="category_edit"),
            ]
        ),
    ),
]
