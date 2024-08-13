from django.db import models
from apps.common.validators import ScreenMethodValidator

from apps.common.models import BaseModel


class Menu(BaseModel):
    validators = [ScreenMethodValidator]

    name = models.CharField(max_length=256)
    type = models.ForeignKey(
        to="menu.MenuType",
        related_name="menus",
        on_delete=models.CASCADE,
        verbose_name="Menu type",
        help_text="Type of the menu",
    )
    start_at = models.DateTimeField(blank=True)
    end_at = models.DateTimeField(blank=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "name"], name="unique_menu_name_type"
            )
        ]

    def __str__(self):
        return f"{self.type} - {self.name}"

    def screen_unique_name_and_type(self):
        if (
            self.__class__.objects.filter(name=self.name, type=self.type)
            .exclude(id=self.id)
            .exists()
        ):
            return "Menu with this name and type already exists."
