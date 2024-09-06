from django.conf import settings
from django.contrib.auth.hashers import make_password

from apps.common.exceptions import LimitExceededException
from apps.common.service import BaseModelService
from ..exceptions import UserDeletionNotAllowedException

from ..models import User


class UserService(BaseModelService):
    model = User
    search_keywords = ["username", "name", "email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def limit_check(self):
        existing_objects_count = self.model.objects.count()
        if existing_objects_count >= settings.MAX_USER_COUNT:
            raise LimitExceededException

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        self.limit_check()

        remove_keys = ["groups", "user_permissions"]
        for key in remove_keys:
            kwargs.pop(key, None)

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if kwargs.get("password", None):
            kwargs["password"] = make_password(kwargs["password"])

        return kwargs, m2m_data

    def create_user(self, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.create(**kwargs)
        return instance

    def update_user(self, user, **kwargs):
        remove_keys = ["username"]
        for key in remove_keys:
            kwargs.pop(key, None)

        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(user, **kwargs)
        return instance

    def get_user_or_create(self, username, first_name, last_name, email):
        user_default_data = dict(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user, created = self.model.objects.get_or_create(
            username=username, defaults=user_default_data
        )
        return user, created

    def delete(self, instance):
        raise UserDeletionNotAllowedException

    def get_staffs(self, **kwargs):
        staffs = self.list(
            **{
                "is_staff": True,
            },
            **kwargs
        )

        return staffs

    def get_user_permissions(self, user):
        # all_permissions = user.get_all_permissions()
        group_permissions = set()
        user_groups = user.groups.all()
        user_permissions = set(user.user_permissions.all())

        for group in user_groups:
            group_permissions.update(group.permissions.all())

        permissions = user_permissions.union(group_permissions)
        return permissions
