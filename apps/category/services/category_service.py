from apps.common.service import BaseModelService
from apps.metadata.services.metadata_service import MetadataService

from ..models.category import Category


class CategoryService(BaseModelService):
    model = Category

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

        if "parent_uuid" in kwargs:
            kwargs["parent_id"] = self.read_by_uuid(uuid_value=kwargs["parent_uuid"]).id
            del kwargs["parent_uuid"]

        if "metadata_uuids" in kwargs:
            metadata_uuids = kwargs.pop("metadata_uuids")
            metadata_ids = []
            for metadata_uuid in metadata_uuids:
                metadata_ids.append(
                    self.metadata_service.read_by_uuid(uuid_value=metadata_uuid).id
                )
            m2m_data["metadata_ids"] = metadata_ids

        return kwargs, m2m_data

    def create_category(self, **kwargs):
        remove_keys = ["code"]

        for key in remove_keys:
            kwargs.pop(key, None)

        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.create(**kwargs)
        if m2m_data:
            instance.metadata.set(m2m_data["metadata_ids"])
        return instance

    def update_category(self, instance, **kwargs):
        remove_keys = ["code"]

        for key in remove_keys:
            kwargs.pop(key, None)

        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        if m2m_data:
            instance.metadata.set(m2m_data["metadata_ids"])
        return instance
