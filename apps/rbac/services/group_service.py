from apps.common.exceptions import ObjectAlreadyExistsException
from apps.common.service import BaseModelService

from ..models import Group


class GroupService(BaseModelService):
    model = Group
    search_keywords = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        return kwargs, m2m_data

    def create_group(self, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        try:
            self.does_object_already_exists(**kwargs)
        except ObjectAlreadyExistsException as ex:
            raise ObjectAlreadyExistsException(errors={"name": ["Group with this name already exists"]}) from ex
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
