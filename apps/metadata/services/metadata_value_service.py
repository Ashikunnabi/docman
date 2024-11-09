from decimal import Decimal
from apps.common.service import BaseModelService
from apps.metadata.exceptions import InvalidFieldValuesException

from ..models import MetadataValue
from ..services.metadata_field_service import MetadataFieldService


class MetadataValueService(BaseModelService):
    model = MetadataValue

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def document_service(self):
        from apps.document.services import DocumentService

        return DocumentService(user=self.user)

    @property
    def metadata_field_service(self):
        return MetadataFieldService(user=self.user)

    def reform_metadata_values(self, metadata_field: dict) -> list:
        metadata_values = []
        field_uuids = list(metadata_field.keys())
        fields = self.metadata_field_service.list(
            uuid__in=",".join(map(str, field_uuids))
        )

        for field_uuid, value in metadata_field.items():
            field = fields.get(uuid=field_uuid)
            metadata_values.append(
                {
                    "field_uuid": field.uuid,
                    f"value_{field.field_type}": value,
                }
            )

        return metadata_values

    def validate_value(self, **kwargs):
        try:
            if "value_integer" in kwargs:
                kwargs["value_integer"] = int(kwargs["value_integer"])
            if "value_decimal" in kwargs:
                kwargs["value_decimal"] = Decimal(kwargs["value_decimal"])
            if "value_boolean" in kwargs:
                kwargs["value_boolean"] = bool(kwargs["value_boolean"])
            if "value_date" in kwargs:
                kwargs["value_date"] = kwargs["value_date"]
            if "value_datetime" in kwargs:
                kwargs["value_datetime"] = kwargs["value_datetime"]
            if "value_time" in kwargs:
                kwargs["value_time"] = kwargs["value_time"]
            if "value_url" in kwargs:
                kwargs["value_url"] = kwargs["value_url"]
            if "value_email" in kwargs:
                kwargs["value_email"] = kwargs["value_email"]
        except Exception as ex:
            raise InvalidFieldValuesException("Invalid value")

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "document_uuid" in kwargs:
            kwargs["document_id"] = self.document_service.read_by_uuid(
                uuid_value=kwargs["document_uuid"]
            ).id
            del kwargs["document_uuid"]

        if "field_uuid" in kwargs:
            kwargs["field_id"] = self.metadata_field_service.read_by_uuid(
                uuid_value=kwargs["field_uuid"]
            ).id
            del kwargs["field_uuid"]

        self.validate_value(**kwargs)

        return kwargs, m2m_data

    def create_metadata_value(self, **kwargs):
        remove_keys = []

        for key in remove_keys:
            del kwargs[key]

        kwargs, m2m_data = self.validated_data(**kwargs)
        return self.create(**kwargs)

    def update_metadata_value(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance

    def create_or_update(self, metadata_values, **kwargs):
        for metadata_value in metadata_values:
            kwargs, m2m_data = self.validated_data(**metadata_value)
            instance = self.list(
                document_id=kwargs["document_id"],
                field_id=kwargs["field_id"],
            ).first()
            if instance:
                self.update_metadata_value(instance, **kwargs)
            else:
                instance = self.create_metadata_value(**kwargs)
