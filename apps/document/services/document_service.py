from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist

from apps.common.exceptions import ObjectNotFoundException
from apps.common.service import BaseModelService

from apps.metadata.services.metadata_value_service import MetadataValueService
from ..exceptions import FileRequiredException
from ..models import Document


class DocumentService(BaseModelService):
    model = Document
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def metadata_value_service(self):
        return MetadataValueService()

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

    def update_metadata_values(self, instance, metadata_values, **kwargs):
        for metadata_value in metadata_values:
            metadata_value["document_uuid"] = instance.uuid
        self.metadata_value_service.create_or_update(metadata_values)
        return instance
