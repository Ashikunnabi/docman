from apps.document.models.document import Document

from apps.menu.models.menu_document import MenuDocument
from rest_framework import serializers

from apps.common.utils.basic import build_media_url

from ...models import Menu, MenuType, MenuItem


class DocumentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class DocumentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "uuid",
            "extension",
            "is_encrypted",
            "is_active",
            "name",
            "file",
        ]


class MenuTypeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = [
            "name",
            "is_active",
        ]


class MenuTypeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = [
            "uuid",
            "name",
            "is_active",
        ]


class MenuInputSerializer(serializers.ModelSerializer):
    type_uuid = serializers.UUIDField()

    class Meta:
        model = Menu
        fields = [
            "name",
            "type_uuid",
            "start_at",
            "end_at",
            "is_active",
        ]


class MenuOutputSerializer(serializers.ModelSerializer):
    document_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            "uuid",
            "name",
            "document_thumbnail",
        ]

    def get_document_thumbnail(self, obj):
        url = ""
        thumbnail = obj.documents.filter(is_thumbnail=True).first()
        if thumbnail:
            url = thumbnail.document.file.url
        return url


class MenuItemInputSerializer(serializers.ModelSerializer):
    menu_uuid = serializers.UUIDField()
    item_uuid = serializers.UUIDField()

    class Meta:
        model = MenuItem
        fields = [
            "menu_uuid",
            "item_uuid",
            "start_at",
            "end_at",
        ]


class MenuItemOutputSerializer(serializers.ModelSerializer):
    menu = MenuOutputSerializer()

    class Meta:
        model = MenuItem
        fields = [
            "uuid",
            "menu",
            "item",
            "start_at",
            "end_at",
            "is_active",
        ]


class MenuDocumentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDocument
        fields = "__all__"


class MenuDocumentOutputSerializer(serializers.ModelSerializer):
    document = DocumentOutputSerializer()

    class Meta:
        model = MenuDocument
        fields = [
            "uuid",
            "type",
            "document",
            "sort_order",
            "is_thumbnail",
        ]


class MenuDocumentUploadInputSerializer(serializers.Serializer):
    file = serializers.FileField()
    is_thumbnail = serializers.BooleanField()
    sort_order = serializers.IntegerField()
