from django.conf import settings
from django.contrib.auth.models import Permission

from apps.common.exceptions import LimitExceededException, ObjectAlreadyExistsException
from apps.common.service import BaseModelService
from apps.rbac.models.branch import User

from ..models import Group


class GroupService(BaseModelService):
    model = Group
    search_keywords = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def limit_check(self):
        existing_objects_count = self.model.objects.count()
        if existing_objects_count >= settings.MAX_GROUP_COUNT:
            raise LimitExceededException

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        self.limit_check()

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                if "permissions" == m2m_key and kwargs.get(m2m_key, []):
                    permission_ids = []
                    for permission_code in kwargs.get(m2m_key):
                        app_label, codename = permission_code.split(".")
                        permission = Permission.objects.get(
                            content_type__app_label=app_label, codename=codename
                        )
                        permission_ids.append(permission.id)
                    permissions = Permission.objects.filter(id__in=permission_ids)
                    kwargs[m2m_key] = permissions
                if "users" == m2m_key:
                    users = User.objects.filter(uuid__in=kwargs.get(m2m_key))
                    kwargs[m2m_key] = users
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        return kwargs, m2m_data

    def create_group(self, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        try:
            self.does_object_already_exists(**kwargs)
        except ObjectAlreadyExistsException as ex:
            raise ObjectAlreadyExistsException(
                errors={"name": ["Group with this name already exists"]}
            ) from ex
        instance = self.create(**kwargs)

        if "permissions" in m2m_data:
            if m2m_data.get("permissions"):
                instance.permissions.set(m2m_data.get("permissions"))
            else:
                instance.permissions.clear()
        if "users" in m2m_data:
            if m2m_data.get("users"):
                instance.user_set.set(m2m_data.get("users"))
            else:
                instance.user_set.clear()
        return instance

    def update_group(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)

        if "permissions" in m2m_data:
            if m2m_data.get("permissions"):
                instance.permissions.set(m2m_data.get("permissions"))
            else:
                instance.permissions.clear()
        if "users" in m2m_data:
            if m2m_data.get("users"):
                instance.user_set.set(m2m_data.get("users"))
            else:
                instance.user_set.clear()
        return instance

    def get_group_or_create(
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
