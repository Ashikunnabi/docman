from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/metadata/', include('apps.metadata.api.v1.urls'))
]
