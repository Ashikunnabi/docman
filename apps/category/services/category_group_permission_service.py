from apps.category.exceptions import CategoryDeleteException
from apps.category.models.category_group_permission import CategoryGroupPermission
from apps.common.service import BaseModelService
from apps.metadata.services.metadata_service import MetadataService


class CategoryGroupPermissionService(BaseModelService):
    model = CategoryGroupPermission

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    @property
    def group_service(self):
        from apps.rbac.services.group_service import GroupService

        return GroupService(user=self.user)

    @property
    def category_service(self):
        from apps.category.services.category_service import (
            CategoryService,
        )

        return CategoryService(user=self.user)
