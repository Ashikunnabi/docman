from apps.common.custom_pagination import LargeResultsSetPagination
from apps.common.exceptions import ObjectNotFoundException
from rest_framework import filters, status
from rest_framework.response import Response

from apps.common.custom_viewset import (
    BaseCreateAPIView,
    BaseListAPIView,
    BaseListCreateAPIView,
    BaseRetrieveUpdateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.document.services.document_service import DocumentService

from .serializers import (
    DocumentInputSerializer,
    DocumentMetadataValueInputSerializer,
    DocumentOutputSerializer,
    DocumentSimpleOutputSerializer,
    DocumentUploadInputSerializer,
)


class DocumentListCreateAPIView(BaseListCreateAPIView):
    service_class = DocumentService
    input_serializer_class = DocumentInputSerializer
    output_serializer_class = DocumentOutputSerializer
    simpleoutput_serializer_class = DocumentSimpleOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.get_service()
        # only list documents created by the user and does not have a category
        queryset = service.list(**{"created_by": request.user, "category": None})
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.simpleoutput_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.simpleoutput_serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        service = self.get_service()
        document = service.create(**validated_data)
        output_serializer = self.get_output_serializer(document)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class DocumentRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = DocumentService
    input_serializer_class = DocumentInputSerializer
    output_serializer_class = DocumentOutputSerializer
    http_method_names = ["get", "delete"]

    def get_object(self):
        instance = super().get_object()
        service = self.get_service(user=self.request.user)
        viewable_category_codes = (
            service.category_permission_service.category_code_permissions()
        )
        if instance.category and instance.category.code not in viewable_category_codes:
            raise ObjectNotFoundException("Document not found")
        return instance

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.get_service()
        service.delete(instance)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response["Content-Length"] = 0
        return response


class DocumentMetadataValueUpdateAPIView(BaseRetrieveUpdateAPIView):
    service_class = DocumentService
    input_serializer_class = DocumentMetadataValueInputSerializer
    output_serializer_class = DocumentOutputSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_input_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        metadata_values = serializer.validated_data
        service = self.get_service()
        document = service.update_metadata_values(instance, metadata_values)
        output_serializer = self.get_output_serializer(document)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class DocumentSearchAPIView(BaseListAPIView):
    service_class = DocumentService
    input_serializer_class = DocumentInputSerializer
    output_serializer_class = DocumentOutputSerializer
    simpleoutput_serializer_class = DocumentSimpleOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.get_service(**{"user": request.user})
        queryset = service.search(**request.query_params.dict())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.simpleoutput_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.simpleoutput_serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentUploadAPIView(BaseCreateAPIView):
    service_class = DocumentService
    input_serializer_class = DocumentUploadInputSerializer
    output_serializer_class = DocumentOutputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        service = self.get_service()
        document = service.document_upload(**validated_data)
        output_serializer = self.get_output_serializer(document, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
