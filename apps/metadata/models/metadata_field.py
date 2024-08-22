from django.db import models

from apps.common.models import BaseModel
from apps.common.validators import ScreenMethodValidator

from ..constants import MetadataFieldType


class MetadataField(BaseModel):
    validators = [ScreenMethodValidator]

    metadata = models.ForeignKey(
        "Metadata",
        on_delete=models.CASCADE,
        related_name="fields",
        help_text="The metadata the field belongs to.",
    )

    code = models.CharField(
        max_length=500,
        help_text="The code of the metadata field.",
    )

    name = models.CharField(
        default="",
        blank=True,
        max_length=500,
        help_text="The name of the metadata field.",
    )
    placeholder = models.CharField(
        default="",
        blank=True,
        max_length=500,
        help_text="The placeholder for the metadata field.",
    )
    field_type = models.CharField(
        max_length=500,
        choices=MetadataFieldType.CHOICES,
        default=MetadataFieldType.TEXT,
        help_text="The type of the metadata field.",
    )
    is_required = models.BooleanField(
        default=False,
        help_text="Whether the metadata field is required or not.",
    )
    is_unique = models.BooleanField(
        default=False,
        help_text="Whether the metadata field value is unique accross the folder or not.",
    )
    order = models.IntegerField(
        default=9999,
        help_text="The order of the metadata field. Lower the order, higher the priority.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["code", "field_type"], name="unique_metadata_code_field_type"
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.field_type}"

    def screen_unique_code_and_field_type(self):
        if (
            self.__class__.objects.filter(code=self.code, field_type=self.field_type)
            .exclude(id=self.id)
            .exists()
        ):
            return "Metadata with this code and field_type already exists."
