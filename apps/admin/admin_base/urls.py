from django.urls import path
from .views import *


app_name = 'admin_base'

urlpatterns = [
    path('', index, name='index'),
]
