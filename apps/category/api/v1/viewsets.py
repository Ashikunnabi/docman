from django.contrib.auth import get_user_model
from apps.category.services.category_group_permission_service import (
    CategoryGroupPermissionService,
)
from rest_framework import filters, status
from rest_framework.response import Response

from apps.common.custom_pagination import LargeResultsSetPagination
from apps.common.custom_viewset import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.common.utils.basic import *

from ...services import CategoryService
from .serializers import (
    CategoryGroupPermissionOutputSerializer,
    CategoryInputSerializer,
    CategoryOutputSerializer,
    SimpleCategoryOutputSerializer,
)

User = get_user_model()


class CategoryListCreateAPIView(BaseListCreateAPIView):
    service_class = CategoryService
    input_serializer_class = CategoryInputSerializer
    output_serializer_class = CategoryOutputSerializer
    simple_output_serializer_class = SimpleCategoryOutputSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def list(self, request, *args, **kwargs):
        service = self.service_class(user=request.user)
        queryset = service.filtered_list()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.simple_output_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.simple_output_serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        instance = service.create_category(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = CategoryService
    input_serializer_class = CategoryInputSerializer
    output_serializer_class = CategoryOutputSerializer

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

        service = self.service_class()
        instance = service.update_category(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response["Content-Length"] = 0
        return response


class CategoryGroupPermissionListCreateAPIView(BaseListCreateAPIView):
    service_class = CategoryGroupPermissionService
    input_serializer_class = CategoryInputSerializer
    output_serializer_class = CategoryGroupPermissionOutputSerializer

    def list(self, request, *args, **kwargs):
        service = self.service_class(user=request.user)
        category = self.service_class(user=request.user).category_service.read_by_uuid(
            uuid_value=kwargs["uuid"]
        )
        queryset = service.group_service.list()
        queryset = self.filter_queryset(queryset)

        serializer = self.output_serializer_class(
            queryset, many=True, context={"category": category}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        instance = service.create_category(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
