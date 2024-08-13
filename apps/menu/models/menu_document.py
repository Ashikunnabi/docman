from django.db import models
from apps.common.validators import ScreenMethodValidator

from apps.document.models import Document
from apps.common.models import BaseModel

from ..constants import MenuDocumentTypes
from .menu import Menu


class MenuDocument(BaseModel):
    validators = [ScreenMethodValidator]

    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="documents"
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="+")
    type = models.CharField(
        choices=MenuDocumentTypes.CHOICES,
        default=MenuDocumentTypes.IMAGE,
        max_length=50,
    )
    is_thumbnail = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.menu}"
