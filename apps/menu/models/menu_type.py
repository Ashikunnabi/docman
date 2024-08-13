from django.db import models
from apps.common.validators import ScreenMethodValidator

from apps.common.models import BaseModel


class MenuType(BaseModel):
    validators = [ScreenMethodValidator]

    name = models.CharField(max_length=256)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_menu_name")
        ]

    def __str__(self):
        return f"- {self.name}"

    def screen_unique_name(self):
        if self.__class__.objects.filter(name=self.name).exclude(id=self.id).exists():
            return "Menu type with this name already exists."
