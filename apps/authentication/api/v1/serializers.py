from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoggedInUserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "uuid",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "is_active",
            "date_joined",
            "is_password_change_required",
            "last_login",
        )
