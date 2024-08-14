from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist

from apps.common.exceptions import ObjectNotFoundException
from apps.common.service import BaseModelService

from ..exceptions import FileRequiredException
from ..models import Document


class DocumentService(BaseModelService):
    model = Document
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read_by_uuid(self, uuid_value, **kwargs):
        try:
            instance = super().read_by_uuid(uuid_value, **kwargs)
        except ObjectDoesNotExist:
            raise ObjectNotFoundException("Document not found")
        return instance

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "file" not in kwargs:
            raise FileRequiredException

        kwargs["name"] = kwargs["file"].name
        kwargs["extension"] = kwargs["file"].name.split(".")[-1]
        kwargs["size"] = kwargs["file"].size

        return kwargs, m2m_data

    def create(self, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = super().create(**kwargs)
        return instance
