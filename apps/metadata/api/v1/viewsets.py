from django.contrib.auth import get_user_model
from rest_framework import filters, status
from rest_framework.response import Response

from apps.common.custom_pagination import LargeResultsSetPagination
from apps.common.custom_viewset import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.common.utils.basic import *
from apps.metadata.services.metadata_field_service import MetadataFieldService

from ...services import MetadataService
from .serializers import (
    MetadataFieldInputSerializer,
    MetadataFieldOutputSerializer,
    MetadataInputSerializer,
    MetadataOutputSerializer,
)

User = get_user_model()


class MetadataListCreateAPIView(BaseListCreateAPIView):
    service_class = MetadataService
    input_serializer_class = MetadataInputSerializer
    output_serializer_class = MetadataOutputSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def list(self, request, *args, **kwargs):
        service = self.service_class(user=request.user)
        queryset = service.list()
        queryset = self.filter_queryset(queryset)

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
        instance = service.create_metadata(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MetadataRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MetadataService
    input_serializer_class = MetadataInputSerializer
    output_serializer_class = MetadataOutputSerializer

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
        instance = service.update_metadata(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class(user=request.user)
        service.delete(instance=instance)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response["Content-Length"] = 0
        return response


class MetadataFieldListCreateAPIView(BaseListCreateAPIView):
    service_class = MetadataFieldService
    input_serializer_class = MetadataFieldInputSerializer
    output_serializer_class = MetadataFieldOutputSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def list(self, request, *args, **kwargs):
        service = self.service_class(user=request.user)
        queryset = service.list()
        queryset = self.filter_queryset(queryset)

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
        validated_data = serializer.validated_data
        validated_data["metadata_uuid"] = kwargs["uuid"]
        instance = service.create_metadata_field(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MetadataFieldRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MetadataFieldService
    input_serializer_class = MetadataFieldInputSerializer
    output_serializer_class = MetadataFieldOutputSerializer

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
        instance = service.update_metadata_field(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class(user=request.user)
        service.delete(instance=instance)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response["Content-Length"] = 0
        return response
