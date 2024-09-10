import re

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response

from .utils.basic import convert_str_date_format


class CreateAPIMixin:
    """
    Create API mixin
    """

    def prepare_raw_data(self, request, *args, **kwargs):
        """
        Prepare data to be saved. By default it's request.data.
        Override this method if you want to update the posted raw data.

        :param request: request
        :param args: additional positional arguments
        :param kwargs: additional keyword arguments
        :return: Data to be saved
        """
        request_data = request.data
        # Write you code here to update raw posted data
        return request_data

    def create(self, request, *args, **kwargs):
        """
        This method overrides the 'create' method of 'CreateModelMixin' class of DRF.
        prepare_raw_data method is used to get raw data instead of request.data.
        :param request: request
        :param args: additional positional arguments
        :param kwargs: additional keyword arguments
        :return: HTTP response with saved data
        """

        raw_data = self.prepare_raw_data(request, *args, **kwargs)
        serializer = self.get_serializer(data=raw_data)
        # TODO: can be done with self.check_serializer, have to check later.
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        #  The following line is commented out because we are not using uuid for now.
        # if serializer.instance:
        #     serializer.data.update({"uuid": serializer.instance.uuid})
        if (
            serializer.instance
            and hasattr(self, "output_serializer_class")
            and self.output_serializer_class
        ):
            output_serializer = self.output_serializer_class(
                serializer.instance, context=self.get_serializer_context()
            )
            headers = self.get_success_headers(output_serializer.data)
            return Response(
                output_serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """
        This method overrides the 'perform_create' method of 'CreateModelMixin' class of DRF.
        'create' method of service will be called instead of serializer.save()
        :param serializer: serializer instance
        :return: None
        """

        assert self.service_class is not None, (
            f"{self.__class__.__name__} should either include a `service_class` attribute, "
            "or override the `perform_create()` method."
        )

        service = self.service_class(user=self.user)

        # TODO: remove this temporary fix to handle database error specially for uniqueness check that is
        # raised after serializer.is_valid()
        try:
            create_data = serializer.validated_data
            serializer.instance = service.create(**create_data)
        except ValidationError as ex:
            if hasattr(ex, "message_dict"):
                raise DRFValidationError(ex.message_dict) from ex
            else:
                raise DRFValidationError(ex) from ex
        except ObjectDoesNotExist as ex:
            raise NotFound(detail=ex) from ex


class RetrieveAPIMixin(object):
    """
    Retrieve API mixin
    """

    def prepare_query_params(self):
        """
        Prepare query parameter dict. By default it's query params of the request. Override this method if you want to
        update the query params.
        :return: prepared query parameters dict
        """
        valid_querystring_pattern = re.compile(r"^[\w\- .,]+$")
        query_params_dict = self.request.query_params.dict()
        for key, val in query_params_dict.items():
            if "-" in val and len(val.split("-")):
                try:
                    query_params_dict[key] = convert_str_date_format(val)
                except ValueError:
                    query_params_dict[key] = val
            if val in ["true", "false"]:
                query_params_dict[key] = True if val == "true" else False
        for key, val in query_params_dict.items():
            if valid_querystring_pattern.match(str(val)) is None:
                raise DRFValidationError({"detail": ["Invalid parameters"]})
        return query_params_dict

    def get_object(self):
        """
        This method overrides the 'get_object' method of 'GenericAPIView' class of DRF.
        'get_by_uuid' method of service class is called to get model instance.
        :return: model instance
        """
        assert self.service_class is not None, (
            "'%s' should either include a `service_class` attribute, "
            "or override the `get_object()` method." % self.__class__.__name__
        )
        query_params = self.prepare_query_params()
        # todo: check if this is what we want
        # Please Note: Previously we have users field in order/cart model, so this check was n't doing anything.
        # But in this PR we renamed that field users to user. So this will cause issues while filtering.
        # FIXME: remove this if we don't want this
        # if self.request.user:
        #     query_params["user"] = self.request.user

        service = self.service_class(user=self.request.user)
        if self.lookup_field == "id":
            pk = self.kwargs.get("id")
            return service.read_by_pk(pk_value=pk, **query_params)
        uuid = self.kwargs.get("uuid")
        return service.read_by_uuid(uuid, **query_params)


class ListAPIMixin(object):
    def prepare_query_params_dict(self):
        """
        Prepare query parameter dict. By default it's query params of the request. Override this method if you want to
        update the query params.
        :return: prepared query parameters dict
        """
        valid_querystring_pattern = re.compile(r"^[\w\- .,@+]+$")
        query_params_dict = self.request.query_params.dict()
        for key, val in query_params_dict.items():
            if "-" in val and len(val.split("-")):
                try:
                    query_params_dict[key] = convert_str_date_format(val)
                except ValueError:
                    query_params_dict[key] = val
            if val in ["true", "false"]:
                query_params_dict[key] = True if val == "true" else False

        if self.request.user:
            query_params_dict["user"] = self.request.user

        for key, val in query_params_dict.items():
            if valid_querystring_pattern.match(str(val)) is None:
                raise DRFValidationError({"detail": ["Invalid parameters"]})
        return query_params_dict

    def mapped_query_params_dict(
        self, query_params_dict: dict, mapped_dict: dict
    ) -> dict:
        params_keys = query_params_dict.keys()
        for key in mapped_dict.keys():
            if key in params_keys:
                query_params_dict[mapped_dict[key]] = query_params_dict.pop(key)
        return query_params_dict

    def get_queryset(self, ignore_user=False):
        """
        This method overrides the 'get_queryset' method of 'GenericAPIView' class of DRF.
        'list' method of service class is called to get queryset.
        Use ignore user if you want to omit the filtering on the user
        :return: queryset
        """
        assert self.service_class is not None, (
            "'%s' should either include a `service_class` attribute, "
            "or override the `get_queryset()` method." % self.__class__.__name__
        )
        query_params_dict = self.prepare_query_params_dict()
        if ignore_user:
            query_params_dict.pop("user")
        service = self.service_class(user=self.user)

        return service.list(**query_params_dict)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, "sort_order"):
            queryset = queryset.order_by(self.sort_order)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


class DashboardAPIPermissionMixin:
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        Check for an extra permission 'IsDashboardUser' for Dashboard APIs
        """
        permissions = super().get_permissions()
        return permissions
