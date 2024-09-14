import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.common.custom_pagination import LargeResultsSetPagination
from apps.common.custom_viewset import (
    BaseListAPIView,
    BaseListCreateAPIView,
    BaseRetrieveAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.common.utils.basic import *
from apps.rbac.api.v1.serializers import (  # UserActivityLogSerializer,
    GroupOutputSerializer,
    GroupInputSerializer,
    PermissionSerializer,
    UserInputSerializer,
    UserOutputSerializer,
    UserPermissionOutputSerializer,
)
from apps.rbac.models import User
from apps.rbac.services import GroupService, UserService
from apps.rbac.services.permission_service import PermissionService


class UserListCreateAPIView(BaseListCreateAPIView):
    service_class = UserService
    input_serializer_class = UserInputSerializer
    output_serializer_class = UserOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class(user=request.user)
        search = {
            "search": request.GET.get("search[value]", request.GET.get("q", None))
        }
        queryset = service.list(**search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class(user=request.user)
        user = service.create_user(**serializer.validated_data)
        serializer = self.get_output_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = UserService
    input_serializer_class = UserInputSerializer
    output_serializer_class = UserOutputSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_input_serializer(
            instance=instance, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        service = self.service_class(user=request.user)
        user = service.update_user(user=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class(user=request.user)
        service.delete(instance=instance)
        return Response(
            {"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class UserPermissionListAPIView(BaseListAPIView):
    service_class = UserService
    input_serializer_class = UserInputSerializer
    output_serializer_class = UserPermissionOutputSerializer

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        permissions = self.service_class(user=request.user).get_user_permissions(user=instance)
        serializer = self.get_output_serializer(permissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCategoryPermissionListAPIView(BaseListAPIView):
    service_class = PermissionService

    def list(self, request, *args, **kwargs):
        permissions = request.user.get_category_permission_codes()
        return Response(permissions, status=status.HTTP_200_OK)


class StaffListAPIView(BaseListAPIView):
    service_class = UserService
    output_serializer_class = UserOutputSerializer

    def list(self, request, *args, **kwargs):
        service = self.service_class(user=request.user)
        search = {
            "search": request.GET.get("search[value]", request.GET.get("q", None))
        }
        queryset = service.get_staffs(**search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
def last_account_activation_email_sent_at(request):
    data = request.query_params.get("id", None)

    # request.data must contain user's uuid. {'id': uuid}
    if not data:
        return Response(
            {"data": "User id not found"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    users = get_user_model().objects.filter(uuid=data)

    # if no user found with given uuid
    if not users.exists():
        return Response({"data": "User id not found"}, status=status.HTTP_404_NOT_FOUND)

    # collect first user
    user = users.first()

    # last_account_activation_email_activity = ActivityLog.objects.filter(
    #     description=f"Email: An account activation email send at '{user.email}'."
    # )

    # if last_account_activation_email_activity.exists():
    #     last_email_sent_at = last_account_activation_email_activity.latest(
    #         "id"
    #     ).created_at
    #     last_email_sent_at = last_email_sent_at.strftime("%d %B, %Y, %H:%M:%S")
    # else:
    #     last_email_sent_at = ""

    return Response({"data": "last_email_sent_at"}, status=status.HTTP_200_OK)


@api_view(http_method_names=["PATCH"])
def update_own_profile_info(request):
    data = request.data.dict()
    files = request.FILES
    try:
        del data["csrfmiddlewaretoken"]
        del data["email"]
    except Exception:
        pass

    # store files in server
    for file in files:
        file_path = f"{settings.USER_INFORMATION_FILE_LOCATION}{files[file].name}"
        path = default_storage.save(file_path, files[file])
        data[file] = path

    # password hash
    if "password" in data.keys():
        data["password"] = make_password(data["password"])

    previous_data_before_update = get_user_model().objects.get(id=request.user.id)
    User.objects.filter(id=request.user.id).update(**data)

    return Response(
        {"data": UserOutputSerializer(request.user).data}, status=status.HTTP_200_OK
    )


@api_view(http_method_names=["GET"])
def active_account_by_activation_url(request):
    refresh_token = request.query_params.get("rt", None)
    activation_url = request.query_params.get("au", None)

    # request.data must contain user's uuid. {'id': uuid}
    if not refresh_token or not activation_url:
        return Response(
            {"data": "Invalid Activation URL"}, status=status.HTTP_404_NOT_FOUND
        )

    # JWT refresh token decode
    try:
        jwt_decoded_data = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
        )
    except Exception as ex:
        return Response(
            {"data": "Invalid Activation URL"}, status=status.HTTP_404_NOT_FOUND
        )

    users = get_user_model().objects.filter(
        id=jwt_decoded_data["user_id"], activation_url=activation_url
    )

    # if no user found with given uuid
    if not users.exists():
        return Response(
            {"data": "Invalid Activation URL"}, status=status.HTTP_404_NOT_FOUND
        )

    # collect first user
    user = users.first()

    # Already active user
    if user.is_active:
        return Response(
            {"data": "Invalid Activation URL"}, status=status.HTTP_404_NOT_FOUND
        )

    # active user account
    user.is_active = True
    user.save()

    return Response({"data": "Account activated"}, status=status.HTTP_200_OK)


class UserActivityLogViewSet(BaseListCreateAPIView, BaseRetrieveUpdateDestroyAPIView):
    pagination_class = LargeResultsSetPagination
    # queryset = ActivityLog.objects.all()
    # model = ActivityLog
    # serializer_class = UserActivityLogSerializer
    lookup_field = "uuid"  # Individual object will be found by this field
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by("-id")
        if not request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DealerViewSet(BaseListCreateAPIView, BaseRetrieveUpdateDestroyAPIView):
    pagination_class = LargeResultsSetPagination
    queryset = User.objects.all()
    model = User
    serializer_class = UserInputSerializer
    lookup_field = "uuid"  # Individual object will be found by this field
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(is_active=True, is_staff=False)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     files = request.FILES
    #
    #     # store files in server
    #     for file in files:
    #         file_path = f'{settings.USER_INFORMATION_FILE_LOCATION}{files[file].name}'
    #         path = default_storage.save(file_path, files[file])
    #         data[file] = path
    #
    #     # password hash
    #     if 'password' in data.keys():
    #         data['password'] = make_password(data['password'])
    #
    #     serializer = self.get_serializer(data=data)
    #     if not serializer.is_valid():
    #         return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    #
    #     self.perform_create(serializer, request)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # def update(self, request, *args, **kwargs):
    #     data = request.data
    #     files = request.FILES
    #
    #     # set to mutable
    #     data._mutable = True
    #     # store files in server
    #
    #     for file in files:
    #         file_path = f'{settings.USER_INFORMATION_FILE_LOCATION}{files[file].name}'
    #         path = default_storage.save(file_path, files[file])
    #         data[file] = path
    #
    #     # password hash
    #     if 'password' in data.keys():
    #         data['password'] = make_password(data['password'])
    #
    #     # set to immutable
    #     data._mutable = False
    #
    #     instance = self.get_object()
    #
    #     serializer = self.get_serializer(instance, data=data, partial=True)
    #     if not serializer.is_valid():
    #         return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    #
    #     self.perform_update(instance, serializer, request)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()  # get the requested object instance
    #     self.perform_destroy(instance, request)
    #     return Response({"detail": "User deleted successfully"}, status=status.HTTP_200_OK)


class GroupListCreateAPIView(BaseListCreateAPIView):
    service_class = GroupService
    input_serializer_class = GroupInputSerializer
    output_serializer_class = GroupOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class(user=request.user)
        search = {
            "search": request.GET.get("search[value]", request.GET.get("q", None))
        }
        queryset = service.list(**search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class(user=request.user)
        group = service.create_group(**serializer.validated_data)
        serializer = self.get_output_serializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = GroupService
    input_serializer_class = GroupInputSerializer
    output_serializer_class = GroupOutputSerializer
    pagination_class = LargeResultsSetPagination
    lookup_field = "id"  # Individual object will be found by this field

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        service = self.service_class(user=request.user)
        group = service.update_group(instance=instance, **serializer.validated_data)
        serializer = self.output_serializer_class(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionListAPIView(BaseListAPIView):
    service_class = PermissionService
    input_serializer_class = PermissionSerializer
    output_serializer_class = PermissionSerializer

    def list(self, request, *args, **kwargs):
        service = self.service_class(user=request.user)
        queryset = service.get_user_permissions_dict()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PermissionRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = PermissionService
    input_serializer_class = PermissionSerializer
    output_serializer_class = PermissionSerializer
    pagination_class = LargeResultsSetPagination
    lookup_field = "id"  # Individual object will be found by this field

    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.get_object()
        if data.get("title") == "":
            instance.title = ""
        if data.get("description") == "":
            instance.description = ""
        if data.get("discount") == "":
            instance.discount = 0
        if data.get("redirect_url") == "":
            instance.redirect_url = ""
        instance.save()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance
        self.perform_destroy(instance, request)
        return Response(
            {"detail": "Permission deleted successfully"}, status=status.HTTP_200_OK
        )
