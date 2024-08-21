from django.db import models


class CategoryPermission(models.Model):
    code = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    category = models.ForeignKey(
        "category.Category",
        on_delete=models.CASCADE,
        related_name="permissions",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["code", "category"], name="unique_category_permission_code"
            )
        ]
        indexes = [
            models.Index(fields=["code"], name="category_permission_code_idx"),
        ]
    
    def __str__(self):
        return f"{self.category.name} | {self.name}"
