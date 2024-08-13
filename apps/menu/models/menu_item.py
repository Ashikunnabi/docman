from django.db import models
from apps.common.validators import ScreenMethodValidator

from apps.common.models import BaseModel


class MenuItem(BaseModel):
    validators = [ScreenMethodValidator]

    menu = models.ForeignKey(
        to="menu.Menu",
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name="Menu",
        help_text="The menu",
    )
    item = models.ForeignKey(
        to="inventory.Product",
        related_name="menus",
        on_delete=models.CASCADE,
        verbose_name="Menu item",
        help_text="Item of the menu",
    )
    start_at = models.DateTimeField(blank=True)
    end_at = models.DateTimeField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["menu", "item"], name="unique_menu_item")
        ]

    def __str__(self):
        return f"{self.menu} - {self.item}"

    def screen_unique_menu_and_item(self):
        if (
            self.__class__.objects.filter(menu=self.menu, item=self.item)
            .exclude(id=self.id)
            .exists()
        ):
            return "Menu item with this menu and item already exists."
