from django.contrib.auth import get_user_model
from apps.menu.services.menu_document_service import MenuDocumentService
from rest_framework import status
from rest_framework.response import Response

from apps.common.custom_pagination import LargeResultsSetPagination
from apps.common.custom_viewset import (
    BaseCreateAPIView,
    BaseListAPIView,
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.common.utils.basic import *

from ...services import MenuService, MenuTypeService, MenuItemService
from .serializers import (
    MenuDocumentInputSerializer,
    MenuDocumentOutputSerializer,
    MenuDocumentUploadInputSerializer,
    MenuInputSerializer,
    MenuItemInputSerializer,
    MenuItemOutputSerializer,
    MenuOutputSerializer,
    MenuTypeInputSerializer,
    MenuTypeOutputSerializer,
)
from rest_framework.permissions import AllowAny


User = get_user_model()


class MenuTypeListCreateAPIView(BaseListCreateAPIView):
    service_class = MenuTypeService
    input_serializer_class = MenuTypeInputSerializer
    output_serializer_class = MenuTypeOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
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

        service = self.service_class()
        instance = service.create_menu_type(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuTypeRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MenuTypeService
    input_serializer_class = MenuTypeInputSerializer
    output_serializer_class = MenuTypeOutputSerializer

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
        instance = service.update_menu_type(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "MenuType deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MenuListAPIView(BaseListAPIView):
    service_class = MenuService
    input_serializer_class = MenuInputSerializer
    output_serializer_class = MenuOutputSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        today = datetime.now().date()
        service = self.service_class()
        extra = {}

        if int(request.GET.get("is_pinned", 0)):
            extra = {
                "is_pinned": True,
            }

        search = {
            "search": request.GET.get("search[value]", request.GET.get("q", None)),
            "is_active": True,
            **extra,
        }
        queryset = service.list(**search)
        queryset = queryset.filter(start_at__date__lte=today, end_at__date__gte=today)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MenuService
    input_serializer_class = MenuInputSerializer
    output_serializer_class = MenuOutputSerializer

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
        instance = service.update_menu(instance=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Menu deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MenuItemListAPIView(BaseListAPIView):
    service_class = MenuItemService
    input_serializer_class = MenuItemInputSerializer
    output_serializer_class = MenuItemInputSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "search": request.GET.get("search[value]", request.GET.get("q", None)),
            "menu__uuid": kwargs.get("menu_uuid"),
        }
        queryset = service.list(**search)
        items = [menu_item.item for menu_item in queryset if service.is_active_menu_item(menu_item_uuid=menu_item.uuid)]

        page = self.paginate_queryset(items)
        if page is not None:
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuItemRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MenuItemService
    input_serializer_class = MenuItemInputSerializer
    output_serializer_class = MenuItemOutputSerializer

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
        instance = service.update_menu_item(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "MenuItem deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MenuDocumentListCreateAPIView(BaseListCreateAPIView):
    service_class = MenuDocumentService
    input_serializer_class = MenuDocumentInputSerializer
    output_serializer_class = MenuDocumentOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "menu__uuid": kwargs["menu_uuid"],
            "search": request.GET.get("search[value]", None),
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

        service = self.service_class()
        instance = service.create_menu_document(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuDocumentRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MenuDocumentService
    input_serializer_class = MenuDocumentInputSerializer
    output_serializer_class = MenuDocumentOutputSerializer

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
        instance = service.update_menu_document(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "MenuDocument deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MenuDocumentUploadAPIView(BaseCreateAPIView):
    service_class = MenuService
    input_serializer_class = MenuDocumentUploadInputSerializer
    output_serializer_class = MenuDocumentOutputSerializer
    pagination_class = LargeResultsSetPagination

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["menu_uuid"] = kwargs["menu_uuid"]

        service = self.service_class()
        instance = service.upload_document(**validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MenuItemSearchListAPIView(BaseListAPIView):
    service_class = MenuItemService
    input_serializer_class = MenuItemInputSerializer
    output_serializer_class = MenuItemInputSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "search": request.GET.get("search", request.GET.get("q", None)),
            "order_by": 0,  # turn off ordering
        }
        queryset = service.list(**search).distinct("item_id")
        items = [menu_item.item for menu_item in queryset]

        page = self.paginate_queryset(items)
        if page is not None:
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)