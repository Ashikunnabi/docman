from django.db import models
from apps.common.validators import ScreenMethodValidator

from apps.common.models import BaseModel


class Category(BaseModel):
    validators = [ScreenMethodValidator]

    name = models.CharField(max_length=256)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    metadata = models.ManyToManyField(
        "metadata.Metadata",
        related_name="categories",
        blank=True,
        null=True,
        default=None,
        help_text="The metadata of the category.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "parent"], name="unique_category_name_parent"
            )
        ]

    def __str__(self):
        return f"{self.name}"

    def screen_unique_name_and_parent(self):
        if (
            self.__class__.objects.filter(name=self.name, parent=self.parent)
            .exclude(id=self.id)
            .exists()
        ):
            return "Category with this name already exists."

    def screen_self_at_parent(self):
        if self.id == self.parent_id:
            return "Parent category cannot be the same as the category itself."
