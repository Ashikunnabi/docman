from django.urls import include, path
from .views import *


app_name = 'admin_rbac'

urlpatterns = [
    path('user/', include([
        path('', user_list, name='user_list'),
        path('add/', user_add, name='user_add'),
        path('edit/<str:uuid>/', user_edit, name='user_edit'),
    ])),
    path('group/', include([
        path('', group_list, name='group_list'),
        path('add/', group_add, name='group_add'),
        path('edit/<int:id>/', group_edit, name='group_edit'),
    ])),

    path('activity-log/', user_activity_log_list, name='user_activity_log_list'),
]
