from pathlib import Path

from apps.common.service import BaseModelService

from ..models import Document


class DocumentService(BaseModelService):
    model = Document
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

    def get_document_details_by_path(self, path, *args, **kwargs):
        path = Path(path)
        data = {
            "name": path.name,
            "file": str(path),
            "extension": str(path.suffix),
            # "size": path.stat().st_size,  # byte
        }
        return data

    def create_document(self, **kwargs):
        path = kwargs["path"]
        data = self.get_document_details_by_path(path=path)
        return self.create(**data)

    def update_document(self, instance, **kwargs):
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
