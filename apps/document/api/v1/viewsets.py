from rest_framework import status
from rest_framework.response import Response

from apps.common.custom_viewset import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.document.services.document_service import DocumentService

from .serializers import DocumentInputSerializer, DocumentOutputSerializer


class DocumentListCreateAPIView(BaseListCreateAPIView):
    service_class = DocumentService
    input_serializer_class = DocumentInputSerializer
    output_serializer_class = DocumentOutputSerializer

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
