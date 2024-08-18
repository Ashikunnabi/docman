from apps.metadata.models.metadata_field import MetadataField
from apps.metadata.models.metadata_value import MetadataValue
from rest_framework import serializers

from ...models import Metadata


class MetadataFieldInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataField
        fields = [
            "name",
            "placeholder",
            "field_type",
            "is_required",
            "is_unique",
            "is_active",
        ]


class MetadataFieldOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetadataField
        fields = [
            "uuid",
            "name",
            "placeholder",
            "field_type",
            "is_required",
            "is_unique",
            "is_active",
        ]


class MetadataInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metadata
        fields = [
            "name",
            "is_active",
        ]


class MetadataOutputSerializer(serializers.ModelSerializer):
    fields = MetadataFieldOutputSerializer(many=True)

    class Meta:
        model = Metadata
        fields = [
            "uuid",
            "name",
            "is_active",
            "fields",
        ]
