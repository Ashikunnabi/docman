from apps.common.service import BaseModelService

from ..models import MetadataField
from .metadata_service import MetadataService


class MetadataFieldService(BaseModelService):
    model = MetadataField

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def metadata_service(self):
        return MetadataService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "metadata_uuid" in kwargs:
            kwargs["metadata_id"] = self.metadata_service.read_by_uuid(
                uuid_value=kwargs["metadata_uuid"]
            ).id
            del kwargs["metadata_uuid"]

        return kwargs, m2m_data

    def create_metadata_field(self, **kwargs):
        remove_keys = []

        for key in remove_keys:
            del kwargs[key]

        kwargs, m2m_data = self.validated_data(**kwargs)
        return self.create(**kwargs)

    def update_metadata_field(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance
