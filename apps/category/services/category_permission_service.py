from apps.category.constants import CategoryPermissionType
from apps.category.exceptions import (
    InvalidCategoryPermissionTypeException,
    UserNotSetException,
)
from apps.category.services.category_service import CategoryService
from apps.common.service import BaseModelService

from ..models.category_permission import CategoryPermission


class CategoryPermissionService(BaseModelService):
    model = CategoryPermission

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def category_service(self):
        return CategoryService(user=self.user)

    def create(self, category, **kwargs):
        for key, value in CategoryPermissionType.CHOICES:
            code = f"{category.code}.{key}_document"
            name = f"Can {key} document of {category.code}"
            self.model.objects.get_or_create(code=code, name=name, category=category)
            print(code)

    def category_code_permissions(self, permission_type="view"):
        valid_permissions = {choice[0] for choice in CategoryPermissionType.CHOICES}

        # Validate the permission type
        if permission_type not in valid_permissions:
            raise InvalidCategoryPermissionTypeException(
                f"Invalid permission type: {permission_type}. Valid choices are: {valid_permissions}"
            )
        if not self.user:
            raise UserNotSetException

        permission_suffix = f".{permission_type}_document"
        suffix_length = len(permission_suffix)

        category_codes = (
            permission[:-suffix_length]
            for permission in self.user.get_category_permission_codes()
            if permission.endswith(permission_suffix)
        )

        return category_codes

    def delete_unnecessary_category_permissions(self):
        queryset = self.list()
        for key, value in CategoryPermissionType.CHOICES:
            queryset = queryset.exclude(code__contains=f".{key}_document")
        queryset.delete()

    def sync_category_permissions(self):
        for category in self.category_service.list():
            self.create(category)
            self.delete_unnecessary_category_permissions()
