from django.urls import include, path


app_name = 'dashboard_api'

urlpatterns = [
    path('v1/dashboard/menus/', include('apps.menu.dashboard_api.v1.urls'))
]
