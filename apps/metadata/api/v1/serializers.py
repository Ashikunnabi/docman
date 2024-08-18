from rest_framework import serializers

from ...models import Metadata


class MetadataInputSerializer(serializers.ModelSerializer):
    parent_uuid = serializers.UUIDField(required=False)

    class Meta:
        model = Metadata
        fields = [
            "name",
            "parent_uuid",
        ]


class SimpleMetadataOutputSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Metadata
        fields = [
            "uuid",
            "name",
            "parent",
            "is_active",
        ]

    def get_parent(self, obj):
        if obj.parent:
            return {
                "uuid": obj.parent.uuid,
                "name": obj.parent.name,
                "parent": obj.parent.parent.uuid if obj.parent.parent else None,
                "is_active": obj.parent.is_active,
            }
        return None


class MetadataOutputSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Metadata
        fields = [
            "uuid",
            "name",
            "parent",
            "is_active",
        ]

    def get_parent(self, obj):
        if obj.parent:
            return MetadataOutputSerializer(obj.parent).data
        return None
