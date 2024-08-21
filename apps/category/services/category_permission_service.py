from apps.category.constants import CategoryPermissionType
from apps.common.service import BaseModelService

from ..models.category_permission import CategoryPermission


class CategoryPermissionService(BaseModelService):
    model = CategoryPermission

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, category, **kwargs):
        for key, value in CategoryPermissionType.CHOICES:
            code = f"category_{category.code}.{key}_document"
            name = f"Can {key} document of {category.code}"
            self.model.objects.get_or_create(code=code, name=name, category=category)
