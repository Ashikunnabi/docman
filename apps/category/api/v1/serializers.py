from rest_framework import serializers

from ...models import Category


class CategoryInputSerializer(serializers.ModelSerializer):
    parent_uuid = serializers.UUIDField(required=False)

    class Meta:
        model = Category
        fields = [
            "name",
            "parent_uuid",
        ]


class SimpleCategoryOutputSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
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


class CategoryOutputSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "uuid",
            "name",
            "parent",
            "is_active",
        ]

    def get_parent(self, obj):
        if obj.parent:
            return CategoryOutputSerializer(obj.parent).data
        return None
