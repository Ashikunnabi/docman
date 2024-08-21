from django.contrib.auth.models import Group
from django.db import models

from apps.common.models import BaseModel


class CategoryGroupPermission(BaseModel):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="category_permissions",
    )
    permission = models.ForeignKey(
        "category.CategoryPermission",
        on_delete=models.CASCADE,
        related_name="category_groups",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "permission"], name="unique_category_group_permission"
            )
        ]

    def __str__(self):
        return self.group.name
