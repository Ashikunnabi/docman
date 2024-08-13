from apps.common.service import BaseModelService

from ..models.menu_type import MenuType


class MenuTypeService(BaseModelService):
    model = MenuType
    search_keywords = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        return kwargs, m2m_data

    def create_menu_type(self, **kwargs):
        remove_keys = []
        for key in remove_keys:
            del kwargs[key]
        return self.create(**kwargs)

    def update_menu_type(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance
