from django.contrib.auth import get_user_model
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


class DocumentOutputSerializer(serializers.ModelSerializer):

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
            "created_by_name",
            "updated_by_name",
        ]
