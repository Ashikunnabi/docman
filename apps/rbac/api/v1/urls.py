from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import *


app_name = "v1"

router = DefaultRouter()
# router.Register(r'user', UserViewSet, basename='user')
# router.Register(r'group', GroupViewSet, basename='group')
# router.Register(r'permission', PermissionViewSet, basename='permission')
# # router.Register(r'user-activity-log', UserActivityLogViewSet, basename='user_activity_log')
# router.Register(r'dealer', DealerViewSet, basename='dealer')

urlpatterns = [
    path(
        "users/",
        include(
            [
                path(
                    "",
                    UserListCreateAPIView.as_view(),
                    name="user_list_create",
                ),
                path(
                    "<uuid:uuid>/",
                    UserRetrieveUpdateDestroyAPIView.as_view(),
                    name="user_retrieve_update_delete",
                ),
                path(
                    "<uuid:uuid>/permissions/",
                    UserPermissionListAPIView.as_view(),
                    name="user_permission_list",
                ),
                path(
                    "staffs/",
                    StaffListAPIView.as_view(),
                    name="staff-list",
                ),
            ]
        ),
    ),
    path("groups/", GroupListCreateAPIView.as_view(), name="group_list_create"),
    path(
        "groups/<int:id>/",
        GroupRetrieveUpdateDestroyAPIView.as_view(),
        name="group_retrieve_update_delete",
    ),
    path(
        "permissions/",
        PermissionListCreateAPIView.as_view(),
        name="permission_list_create",
    ),
    # path(
    #     'permisisons/<int:id>/',
    #     PermissionRetrieveUpdateDestroyAPIView.as_view(),
    #     name='permission_retrieve_update_delete'
    # ),
    path("update-info", update_own_profile_info, name="update_own_profile_info"),
    path(
        "last-account-activation-email-sent-at",
        last_account_activation_email_sent_at,
        name="last_account_activation_email_sent_at",
    ),
    path(
        "account-activate",
        active_account_by_activation_url,
        name="active_account_by_activation_url",
    ),
    path("", include(router.urls)),
]
