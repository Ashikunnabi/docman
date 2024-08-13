from django.urls import include, path
from .views import *


app_name = 'send_email'

urlpatterns = [
    path('api/', include('apps.email.api.urls'), name='api'),
]
