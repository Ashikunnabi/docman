from django.urls import path, include


app_name = 'admin'


urlpatterns = [
    path('', include('apps.admin.admin_base.urls')),
    path('rbac/', include('apps.admin.admin_rbac.urls')),
    path('', include('apps.admin.admin_menu.urls')),
    path('', include('apps.admin.admin_document.urls')),
    path('', include('apps.admin.admin_category.urls')),
    path('', include('apps.admin.admin_metadata.urls')),
]
