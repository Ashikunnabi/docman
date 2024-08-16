from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/categories/', include('apps.category.api.v1.urls'))
]
