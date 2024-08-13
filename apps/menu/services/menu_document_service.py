from apps.common.service import BaseModelService

from ..models import MenuDocument


class MenuDocumentService(BaseModelService):
    model = MenuDocument
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        return kwargs, m2m_data

    def create_menu_document(self, **kwargs):
        remove_keys = []
        for key in remove_keys:
            del kwargs[key]
        return self.create(**kwargs)

    def update_menu_document(self, instance, **kwargs):
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
