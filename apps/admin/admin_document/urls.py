from django.urls import include, path
from .views import *


app_name = 'admin_document'

urlpatterns = [
    path('document/', include([
        path('', document_list, name='document_list'),
        path('edit/<uuid:uuid>/', document_edit, name='document_edit'),
        path('upload/', document_add, name='document_add'),
    ])),
]
