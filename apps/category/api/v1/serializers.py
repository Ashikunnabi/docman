from rest_framework import serializers

from apps.category.constants import CategoryPermissionType
from apps.metadata.api.v1.serializers import MetadataOutputSerializer
from apps.rbac.models import Group

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
    path = serializers.CharField()
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "uuid",
            "code",
            "name",
            "path",
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
    path = serializers.CharField()
    parent = serializers.SerializerMethodField()
    metadata = MetadataOutputSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            "uuid",
            "code",
            "name",
            "path",
            "parent",
            "is_active",
            "metadata",
        ]

    def get_parent(self, obj):
        if obj.parent:
            return CategoryOutputSerializer(obj.parent).data
        return None


class CategoryGroupPermissionInputSerializer(serializers.Serializer):
    permission_id = serializers.IntegerField()
    group_id = serializers.IntegerField()


class CategoryGroupPermissionOutputSerializer(serializers.ModelSerializer):
    permission_names = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "permission_names",
            "permissions",
        ]

    def get_permission_names(self, obj):
        return CategoryPermissionType.CHOICES

    def get_permissions(self, obj):
        category = self.context.get("category")
        if not category:
            raise ValueError("Category is required in context")

        permissions = []
        for key, value in CategoryPermissionType.CHOICES:
            category_permission = category.permissions.filter(
                code__icontains=f".{key}_document"
            ).first()
            if category_permission:
                category_group_permission = obj.category_permissions.filter(
                    permission=category_permission
                ).first()
                if category_group_permission:
                    permissions.append(
                        {
                            "key": key,
                            "group_id": obj.id,
                            "has_permission": True,
                            "category_permission_id": category_permission.id,
                            "category_group_permission_uuid": category_group_permission.uuid,
                        }
                    )
                    continue
                permissions.append(
                    {
                        "key": key,
                        "group_id": obj.id,
                        "has_permission": False,
                        "category_permission_id": category_permission.id,
                        "category_group_permission_uuid": None,
                    }
                )
        return permissions
