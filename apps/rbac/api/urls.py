from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/rbac/', include('apps.rbac.api.v1.urls'))
]
