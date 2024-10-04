from django.urls import include, path

app_name = "apps"

fe_urlpatterns = []

dashboard_urlpatterns = [
    path("", include("apps.authentication.urls")),
    path("", include("apps.common.urls")),
    path("", include("apps.document.urls")),
    path("", include("apps.rbac.urls")),
    path("", include("apps.email.urls")),
    path("", include("apps.category.urls")),
    path("", include("apps.metadata.urls")),
    path("", include("apps.search.urls")),
]

urlpatterns = fe_urlpatterns + dashboard_urlpatterns
