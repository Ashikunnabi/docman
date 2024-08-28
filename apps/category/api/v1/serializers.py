from apps.metadata.api.v1.serializers import MetadataOutputSerializer
from rest_framework import serializers

from ...models import Category


class CategoryInputSerializer(serializers.ModelSerializer):
    parent_uuid = serializers.UUIDField(required=False)
    metadata_uuids = serializers.ListField(
        child=serializers.UUIDField(), required=False
    )

    class Meta:
        model = Category
        fields = [
            "name",
            "parent_uuid",
            "metadata_uuids",
            "is_active",
        ]


class SimpleCategoryOutputSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "uuid",
            "code",
            "name",
            "parent",
            "is_active",
        ]

    def get_parent(self, obj):
        if obj.parent:
            return {
                "uuid": obj.parent.uuid,
                "code": obj.parent.code,
                "name": obj.parent.name,
                "parent": obj.parent.parent.uuid if obj.parent.parent else None,
                "is_active": obj.parent.is_active,
            }
        return None


class CategoryOutputSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    metadata = MetadataOutputSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            "uuid",
            "code",
            "name",
            "parent",
            "is_active",
            "metadata",
        ]

    def get_parent(self, obj):
        if obj.parent:
            return CategoryOutputSerializer(obj.parent).data
        return None
