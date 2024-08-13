from rest_framework import serializers


class LoginInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
