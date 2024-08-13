from django.db import models

from apps.common.models import BaseModel


class Document(BaseModel):
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to="uploads/%Y/%m/%d/", null=True)
    extension = models.CharField(max_length=256)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    is_encrypted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
