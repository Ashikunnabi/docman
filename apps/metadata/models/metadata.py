from django.db import models
from apps.common.validators import ScreenMethodValidator

from apps.common.models import BaseModel


class Metadata(BaseModel):
    validators = [ScreenMethodValidator]

    name = models.CharField(max_length=500, blank=True, default="")
    fields = models.ManyToManyField(
        "metadata.MetadataField", related_name="metadata"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_metadata_name")
        ]

    def __str__(self):
        return f"{self.name}"

    def screen_unique_name(self):
        if self.__class__.objects.filter(name=self.name).exclude(id=self.id).exists():
            return "Metadata with this name already exists."
