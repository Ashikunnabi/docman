from django.contrib.auth import get_user_model
from apps.document.models.document import Document
from apps.metadata.api.v1.serializers import MetadataValueOutputSerializer
from rest_framework import serializers


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
