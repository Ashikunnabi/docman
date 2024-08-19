from decimal import Decimal
from django.db import models

from apps.common.models import BaseModel
from apps.common.validators import ScreenMethodValidator
from apps.metadata.models.metadata_field import MetadataField

from ..constants import MetadataFieldType


class MetadataValue(BaseModel):
    validators = [ScreenMethodValidator]

    document = models.ForeignKey(
        "document.Document",
        on_delete=models.CASCADE,
        related_name="metadata_values",
        help_text="The document that the metadata value belongs to.",
    )
    field = models.ForeignKey(
        MetadataField,
        on_delete=models.CASCADE,
        related_name="values",
        help_text="The metadata field that the value belongs to.",
    )
    value_text = models.TextField(
        blank=True,
        null=True,
        help_text="The text value of the metadata field.",
    )
    value_integer = models.IntegerField(
        blank=True,
        null=True,
        help_text="The integer value of the metadata field.",
    )
    value_decimal = models.DecimalField(
        blank=True,
        null=True,
        max_digits=18,
        decimal_places=2,
        help_text="The decimal value of the metadata field.",
    )
    value_boolean = models.BooleanField(
        blank=True,
        null=True,
        help_text="The boolean value of the metadata field.",
    )
    value_date = models.DateField(
        blank=True,
        null=True,
        help_text="The date value of the metadata field.",
    )
    value_datetime = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The datetime value of the metadata field.",
    )
    value_time = models.TimeField(
        blank=True,
        null=True,
        help_text="The time value of the metadata field.",
    )
    value_url = models.URLField(
        blank=True,
        null=True,
        help_text="The URL value of the metadata field.",
    )
    value_email = models.EmailField(
        blank=True,
        null=True,
        help_text="The email value of the metadata field.",
    )
    value_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="The phone value of the metadata field.",
    )
    value_image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        help_text="The image value of the metadata field.",
    )
    value_file = models.FileField(
        upload_to="files/",
        blank=True,
        null=True,
        help_text="The file value of the metadata field.",
    )
    value_html = models.TextField(
        blank=True,
        null=True,
        help_text="The HTML value of the metadata field.",
    )
    value_markdown = models.TextField(
        blank=True,
        null=True,
        help_text="The Markdown value of the metadata field.",
    )
    value_color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="The color value of the metadata field.",
    )
    value_color_hex = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text="The hex color value of the metadata field.",
    )  # For hex color codes
    value_password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="The password value of the metadata field.",
    )  # Typically hashed
    value_secret = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="The secret value of the metadata field.",
    )  # Typically hashed
    value_percentage = models.FloatField(
        blank=True,
        null=True,
        help_text="The percentage value of the metadata field.",
    )
    value_rating = models.IntegerField(
        blank=True,
        null=True,
        help_text="The rating value of the metadata field.",
    )
    value_country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="The country value of the metadata field.",
    )
    value_language = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="The language value of the metadata field.",
    )
    value_timezone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="The timezone value of the metadata field.",
    )
    value_currency_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="The currency code value of the metadata field.",
    )

    def get_value(self):
        field_type = self.field.field_type
        if field_type == MetadataFieldType.TEXT:
            return self.value_text
        elif field_type == MetadataFieldType.INTEGER:
            return self.value_integer
        elif field_type == MetadataFieldType.DECIMAL:
            return self.value_decimal
        elif field_type == MetadataFieldType.BOOLEAN:
            return self.value_boolean
        elif field_type == MetadataFieldType.DATE:
            return self.value_date
        elif field_type == MetadataFieldType.DATETIME:
            return self.value_datetime
        elif field_type == MetadataFieldType.TIME:
            return self.value_time
        elif field_type == MetadataFieldType.URL:
            return self.value_url
        elif field_type == MetadataFieldType.EMAIL:
            return self.value_email
        elif field_type == MetadataFieldType.PHONE:
            return self.value_phone
        elif field_type == MetadataFieldType.IMAGE:
            return self.value_image
        elif field_type == MetadataFieldType.FILE:
            return self.value_file
        elif field_type == MetadataFieldType.HTML:
            return self.value_html
        elif field_type == MetadataFieldType.MARKDOWN:
            return self.value_markdown
        elif field_type == MetadataFieldType.COLOR:
            return self.value_color
        elif field_type == MetadataFieldType.COLOR_HEX:
            return self.value_color_hex
        elif field_type == MetadataFieldType.PASSWORD:
            return self.value_password
        elif field_type == MetadataFieldType.SECRET:
            return self.value_secret
        elif field_type == MetadataFieldType.PERCENTAGE:
            return self.value_percentage
        elif field_type == MetadataFieldType.RATING:
            return self.value_rating
        elif field_type == MetadataFieldType.COUNTRY:
            return self.value_country
        elif field_type == MetadataFieldType.LANGUAGE:
            return self.value_language
        elif field_type == MetadataFieldType.TIMEZONE:
            return self.value_timezone
        elif field_type == MetadataFieldType.CURRENCY_CODE:
            return self.value_currency_code
        return None

    def __str__(self):
        return f"{self.document.name} - {self.field.name}: {self.get_value()}"

    def screen_unique_type_and_value(self):
        """
        Validate field values based on the field type.
        """
        if self.field.field_type == MetadataFieldType.INTEGER and not isinstance(
            self.value_integer, int
        ):
            return "Invalid integer value"
        if self.field.field_type == MetadataFieldType.DECIMAL and not isinstance(
            self.value_float, Decimal
        ):
            return "Invalid decimal value"
        if self.field.field_type == MetadataFieldType.BOOLEAN and not isinstance(
            self.value_boolean, bool
        ):
            return "Invalid boolean value"
        if self.field.field_type == MetadataFieldType.PERCENTAGE and not (
            0 <= self.value_percentage <= 100
        ):
            return "Percentage value must be between 0 and 100"
        if self.field.field_type == MetadataFieldType.RATING and not (
            1 <= self.value_rating <= 5
        ):
            return "Rating value must be between 1 and 5"
        if self.field.field_type == MetadataFieldType.COLOR_HEX and not (
            self.value_color.startswith("#") and len(self.value_color) == 7
        ):
            return "Invalid color hex value"

    def screen_document_and_field(self):
        """
        Validate that the metadata value does not already exist
        """
        if (
            self.__class__.objects.filter(document=self.document, field=self.field)
            .exclude(id=self.id)
            .exists()
        ):
            return "Metadata value already exists"
