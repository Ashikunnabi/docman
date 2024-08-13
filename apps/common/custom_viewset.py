from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions

from apps.common.exceptions import (
    InputSerializerNotFoundException,
    OutputSerializerNotFoundException,
    ServiceClassNotFoundException,
)

from .api_mixins import (
    CreateAPIMixin,
    DashboardAPIPermissionMixin,
    ListAPIMixin,
    RetrieveAPIMixin,
)


class BaseGenericAPIView:
    lookup_field = "uuid"  # Individual object will be found by this field
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if (
            self.request.method == "GET"
            and hasattr(self, "output_serializer_class")
            and self.output_serializer_class
        ):
            return self.output_serializer_class
        return self.input_serializer_class

    def get_service(self, **kwargs):
        if hasattr(self, "service_class") and self.service_class:
            return self.service_class(**kwargs)
        raise ServiceClassNotFoundException

    def get_input_serializer(self, **kwargs):
        if hasattr(self, "input_serializer_class") and self.input_serializer_class:
            return self.input_serializer_class(**kwargs)
        raise InputSerializerNotFoundException

    def get_output_serializer(self, instance, **kwargs):
        if hasattr(self, "output_serializer_class") and self.output_serializer_class:
            return self.output_serializer_class(instance=instance, **kwargs)
        raise OutputSerializerNotFoundException

    def set_paginated_kwargs(self, **kwargs):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.set_paginated_kwargs(**kwargs)


class BaseListAPIView(BaseGenericAPIView, ListAPIMixin, generics.ListAPIView):
    """
    Base list API view. If model fields are present in querystring then queryset will be filtered automatically by the
    values of those fields.
    """

    service_class = None


class BaseCreateAPIView(BaseGenericAPIView, CreateAPIMixin, generics.CreateAPIView):
    """
    Base create API
    """

    service_class = None
    output_serializer_class = None


class BaseListCreateAPIView(
    BaseGenericAPIView, ListAPIMixin, CreateAPIMixin, generics.ListCreateAPIView
):
    """
    Base list and create API
    """

    service_class = None


class BaseRetrieveAPIView(
    BaseGenericAPIView, RetrieveAPIMixin, generics.RetrieveAPIView
):
    """
    Base retrieve API
    """

    service_class = None


class BaseRetrieveUpdateAPIView(
    BaseGenericAPIView, RetrieveAPIMixin, generics.RetrieveUpdateAPIView
):
    """
    Base retrieve and update API
    """

    service_class = None


class BaseRetrieveUpdateDestroyAPIView(
    BaseGenericAPIView, RetrieveAPIMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    Base retrieve, update and destroy API
    """

    service_class = None


class BaseUpdateAPIView(BaseGenericAPIView, generics.UpdateAPIView):
    """
    Base Update API View
    """

    service_class = None


class BaseDashboardListAPIView(DashboardAPIPermissionMixin, BaseListAPIView):
    """
    Base list API view for dashboard.
    """

    # When new permission classes are set via the permission_classes attribute or decorators
    # we're telling the view to ignore the default list set in the settings.py file.
    # But Default permissions are mandatory
    # permission_classes = [IsAuthenticated, IsDashboardUser]


class BaseDashboardCreateAPIView(DashboardAPIPermissionMixin, BaseCreateAPIView):
    """
    Base Create APIView
    """


class BaseDashboardListCreateAPIView(
    DashboardAPIPermissionMixin, BaseListCreateAPIView
):
    """
    Base list create API view for dashboard.
    """

    # When new permission classes are set via the permission_classes attribute or decorators
    # we're telling the view to ignore the default list set in the settings.py file.
    # But Default permissions are mandatory
    # permission_classes = [IsAuthenticated, IsDashboardUser]


class BaseDashboardRetrieveUpdateDestroyAPIView(
    DashboardAPIPermissionMixin, BaseRetrieveUpdateDestroyAPIView
):
    """
    Base retrieve, update and destroy API.
    """

    # When new permission classes are set via the permission_classes attribute or decorators
    # we're telling the view to ignore the default list set in the settings.py file.
    # But Default permissions are mandatory
    # permission_classes = [IsAuthenticated, IsDashboardUser]


class BaseDashboardRetrieveUpdateAPIView(
    DashboardAPIPermissionMixin, BaseRetrieveUpdateAPIView
):
    """
    Base retrieve, update API view for dashboard..
    """


class BaseDashboardRetrieveAPIView(DashboardAPIPermissionMixin, BaseRetrieveAPIView):
    """
    Base retrieve API view for dashboard..
    """


class DashboardGenericAPIView(DashboardAPIPermissionMixin, BaseGenericAPIView, APIView):
    """
    Base Generic API View for Dashboard.
    It can be responsible for any non-rest API call.
    """


class BaseDashboardUpdateAPIView(DashboardAPIPermissionMixin, BaseUpdateAPIView):
    """
    Base dashboard update API view for dashboard..
    """
