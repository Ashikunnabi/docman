import uuid
from datetime import datetime

from django.db import models

from apps.common.models import BaseModel


def file_location(instance, filename):
    extension = filename.split(".")[-1]
    date_str = datetime.now().strftime("%Y/%m/%d")
    return f"uploads/documents/{date_str}/{uuid.uuid4()}.{extension}"


class Document(BaseModel):
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to=file_location, null=True)
    extension = models.CharField(max_length=256)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    is_encrypted = models.BooleanField(default=False)
    category = models.ForeignKey(
        "category.Category",
        on_delete=models.PROTECT,
        related_name="documents",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    @property
    def category_wise_file_path(self):
        # document has category which has parent category which has parent category and so on
        path = []
        category = self.category
        while category:
            path.append(category.name)
            category = category.parent
        path.reverse()
        return "/".join(path)
