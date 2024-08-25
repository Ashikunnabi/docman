from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


User = get_user_model()


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "username",
            "name",
            "email",
            "phone",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "last_login",
            "date_joined",
            "created_at",
            "updated_at",
            "is_password_change_required",
            "password_updated_at",
            "is_user_locked",
            "user_locked_at",
            "last_login",
            "last_unsuccessful_login",
            "unsuccessful_login_attempts",
        ]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            "name",
            "codename",
        ]


class GroupInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    permissions = serializers.ListField(child=serializers.CharField(), required=False)
    users = serializers.ListField(child=serializers.UUIDField(), required=False)


class GroupOutputSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    users = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"

    def get_users(self, obj):
        return UserOutputSerializer(instance=obj.user_set, many=True).data


class UserPermissionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            "name",
            "codename",
        ]
