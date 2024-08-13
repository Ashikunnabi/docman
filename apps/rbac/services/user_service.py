from django.contrib.auth.hashers import make_password

from apps.common.service import BaseModelService

from ..models import User


class UserService(BaseModelService):
    model = User
    search_keywords = ["username", "name", "email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if kwargs.get("password", None):
            kwargs["password"] = make_password(kwargs["password"])

        return kwargs, m2m_data


    def create_user(self, **kwargs):
        remove_keys = ["groups", "user_permissions"]
        for key in remove_keys:
            del kwargs[key]
        kwargs["password"] = make_password('kwargs["password"]')
        return self.create(**kwargs)

    def update_user(self, user, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(user, **kwargs)
        return instance

    def get_user_or_create(
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

    def get_staffs(self, **kwargs):
        staffs = self.list(
            **{
                "is_staff": True,
            },
            **kwargs
        )

        return staffs
