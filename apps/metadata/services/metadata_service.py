from apps.common.service import BaseModelService

from ..models import Metadata


class MetadataService(BaseModelService):
    model = Metadata

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "parent_uuid" in kwargs:
            kwargs["parent_id"] = self.read_by_uuid(uuid_value=kwargs["parent_uuid"]).id
            del kwargs["parent_uuid"]

        return kwargs, m2m_data

    def create_metadata(self, **kwargs):
        remove_keys = []

        for key in remove_keys:
            del kwargs[key]

        kwargs, m2m_data = self.validated_data(**kwargs)
        return self.create(**kwargs)

    def update_metadata(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance
