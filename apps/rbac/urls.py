from django.urls import include, path
from .views import *


app_name = 'rbac'

urlpatterns = [
    path('api/', include('apps.rbac.api.urls'), name='api'),
]
