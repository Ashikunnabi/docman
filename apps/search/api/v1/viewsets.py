from apps.common.custom_pagination import LargeResultsSetPagination
from rest_framework import filters, status
from rest_framework.response import Response

from apps.common.custom_viewset import (
    BaseListAPIView,
)
from ...services.document_service import DocumentService

from .serializers import (
    DocumentOutputSerializer,
)


class DocumentSearchAPIView(BaseListAPIView):
    service_class = DocumentService
    input_serializer_class = None
    output_serializer_class = DocumentOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.get_service(user=request.user)
        query_params = request.query_params.dict()
        queryset = service.search(**query_params)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.output_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.output_serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
