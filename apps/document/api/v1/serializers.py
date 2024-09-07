from django.contrib.auth import get_user_model
from apps.metadata.api.v1.serializers import MetadataValueOutputSerializer
from apps.metadata.models.metadata_value import MetadataValue
from rest_framework import serializers

from ...models import Document


class DocumentInputSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    name = serializers.CharField(required=False)
    is_encrypted = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Document
        fields = (
            "name",
            "file",
            "is_encrypted",
        )

    def validate(self, data):
        if "name" not in data:
            data["name"] = data["file"].name
        data["extension"] = data["file"].name.split(".")[-1]
        data["size"] = data["file"].size
        return data


class DocumentSimpleOutputSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "uuid",
            "name",
            "file",
            "extension",
            "size",
            "is_active",
            "is_encrypted",
            "created_at",
            "updated_at",
            "category",
            "created_by_name",
            "updated_by_name",
        ]

    def get_category(self, obj):
        if isinstance(obj, Document):
            return obj.category.code if obj.category else None
        return obj.get("category", None)


class DocumentOutputSerializer(serializers.ModelSerializer):
    metadata_values = MetadataValueOutputSerializer(many=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "uuid",
            "name",
            "file",
            "extension",
            "size",
            "is_active",
            "is_encrypted",
            "category",
            "created_at",
            "updated_at",
            "created_by_name",
            "updated_by_name",
            "metadata_values",
        ]

    def get_category(self, obj):
        data = {}
        if obj.category:
            data = {
                "uuid": obj.category.uuid,
                "name": obj.category.name,
                "code": obj.category.code,
                "path": obj.category.path,
            }
        return data


class DocumentMetadataValueInputSerializer(serializers.ModelSerializer):
    field_uuid = serializers.UUIDField(required=True)

    class Meta:
        model = MetadataValue
        fields = [
            "uuid",
            "field_uuid",
            "value_text",
            "value_integer",
            "value_decimal",
            "value_boolean",
            "value_date",
            "value_datetime",
            "value_time",
            "value_url",
            "value_email",
            "value_phone",
            "value_image",
            "value_file",
            "value_html",
            "value_markdown",
            "value_color",
            "value_color_hex",
            "value_password",
            "value_secret",
            "value_percentage",
            "value_rating",
            "value_country",
            "value_language",
            "value_timezone",
            "value_currency_code",
        ]


class DocumentUploadInputSerializer(serializers.Serializer):
    document_uuids = serializers.ListField(child=serializers.UUIDField(), required=True)
    category_uuid = serializers.UUIDField(required=True)
    metadata = serializers.DictField(required=False)
