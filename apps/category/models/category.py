from django.conf import settings
from django.db import models
from apps.common.exceptions import LimitExceededException
from apps.common.utils.basic import random_hex_code
from apps.common.validators import ScreenMethodValidator

from apps.common.models import BaseModel


class Category(BaseModel):
    validators = [ScreenMethodValidator]

    code = models.CharField(max_length=256, unique=True, default=random_hex_code)
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="subcategories",
    )
    metadata = models.ManyToManyField(
        "metadata.Metadata",
        related_name="categories",
        blank=True,
        default=None,
        help_text="The metadata of the category.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "parent"], name="unique_category_name_parent"
            )
        ]
        indexes = [
            models.Index(fields=["code"], name="category_code_idx"),
        ]

    def __str__(self):
        return f"{self.name}"
    
    def screen_limit_check(self):
        existing_objects_count = self.__class__.objects.count()
        if existing_objects_count >= settings.MAX_CATEGORY_COUNT:
            raise LimitExceededException

    def screen_unique_name_and_parent(self):
        if (
            self.__class__.objects.filter(name=self.name, parent=self.parent)
            .exclude(id=self.id)
            .exists()
        ):
            return "Category with this name already exists."

    @property
    def path(self):
        path = []
        instance = self
        while instance:
            path.append(instance.name)
            instance = instance.parent
        return " > ".join(reversed(path))
