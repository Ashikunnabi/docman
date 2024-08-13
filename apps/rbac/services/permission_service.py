from apps.common.service import BaseModelService

from ..models import Permission


class PermissionService(BaseModelService):
    model = Permission
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_permission(self, **kwargs):
        remove_keys = []
        for key in remove_keys:
            del kwargs[key]
        return self.create(**kwargs)

    def update_permission(self, user, **kwargs):
        return self.update_model_instance(user, **kwargs)

    def get_permission_or_create(
        self, username, name, first_name, last_name, email, is_gui=False
    ):
        user_default_data = dict(
            name=name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_gui=is_gui,
        )
        user, created = self.model.objects.get_or_create(
            username=username, defaults=user_default_data
        )
        return user, created
