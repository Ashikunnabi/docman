from apps.category.exceptions import CategoryDeleteException
from apps.common.service import BaseModelService
from apps.metadata.services.metadata_service import MetadataService

from ..models.category import Category, models


class CategoryService(BaseModelService):
    model = Category

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def metadata_service(self):
        return MetadataService(user=self.user)

    @property
    def category_permissions_service(self):
        from apps.category.services.category_permission_service import (
            CategoryPermissionService,
        )

        return CategoryPermissionService(user=self.user)

    def filtered_list(self, **kwargs):
        """Returns the list of categories based on the ADD permissions of the user."""
        queryset = self.list()
        allowed_categories = (
            self.category_permissions_service.category_code_permissions(
                permission_type="add"
            )
        )
        queryset = queryset.filter(code__in=allowed_categories)
        return queryset

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

    def delete(self, instance):
        try:
            super().delete(instance)
        except models.ProtectedError as ex:
            message = "Category can't be deleted. It has documents or subcategories associated with it."
            raise CategoryDeleteException(message)

    def validate_category_metadata_fields(self, category_uuid, metadata_uuids):
        category = self.read_by_uuid(category_uuid)
        connected_metadata_fields = (
            category.metadata.all()
            .prefetch_related("fields")
            .values_list("fields__uuid", flat=True)
        )

        # Convert the list of connected metadata fields to a set for O(1) membership checking
        connected_metadata_field_set = set(map(str, connected_metadata_fields))

        # Check if all provided metadata_uuids are in the set of connected metadata fields
        missing_uuids = [
            uuid for uuid in metadata_uuids if uuid not in connected_metadata_field_set
        ]
        if missing_uuids:
            raise Exception(
                f"Metadata fields not connected to the category: {', '.join(missing_uuids)}"
            )

        return True
