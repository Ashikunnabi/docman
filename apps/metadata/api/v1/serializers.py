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
            "order",
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
            "order",
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


class MetadataValueOutputSerializer(serializers.ModelSerializer):
    field = MetadataFieldOutputSerializer()

    class Meta:
        model = MetadataValue
        fields = [
            "uuid",
            "field",
            "value_text",
            "value_integer",
            "value_decimal",
            "value_boolean",
            "value_date",
            "value_datetime",
            "value_time",
            "value_url",
            "value_email",
            "value_phone",
            "value_image",
            "value_file",
            "value_html",
            "value_markdown",
            "value_color",
            "value_color_hex",
            "value_password",
            "value_secret",
            "value_percentage",
            "value_rating",
            "value_country",
            "value_language",
            "value_timezone",
            "value_currency_code",
        ]
