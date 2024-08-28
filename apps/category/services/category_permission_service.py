from apps.category.constants import CategoryPermissionType
from apps.category.exceptions import (
    InvalidCategoryPermissionTypeException,
    UserNotSetException,
)
from apps.common.service import BaseModelService

from ..models.category_permission import CategoryPermission


class CategoryPermissionService(BaseModelService):
    model = CategoryPermission

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        return self._user

    def create(self, category, **kwargs):
        for key, value in CategoryPermissionType.CHOICES:
            code = f"{category.code}.{key}_document"
            name = f"Can {key} document of {category.code}"
            self.model.objects.get_or_create(code=code, name=name, category=category)

    def category_code_permissions(self, permission_type="view"):
        valid_permissions = {choice[0] for choice in CategoryPermissionType.CHOICES}

        # Validate the permission type
        if permission_type not in valid_permissions:
            raise InvalidCategoryPermissionTypeException(
                f"Invalid permission type: {permission_type}. Valid choices are: {valid_permissions}"
            )
        if not self._user:
            raise UserNotSetException

        permission_suffix = f".{permission_type}_document"
        suffix_length = len(permission_suffix)

        category_codes = (
            permission[:-suffix_length]
            for permission in self._user.get_category_permissions()
            if permission.endswith(permission_suffix)
        )

        return category_codes
