from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist

from apps.category.services.category_permission_service import CategoryPermissionService
from apps.category.services.category_service import CategoryService
from apps.common.exceptions import ObjectNotFoundException
from apps.common.service import BaseModelService

from apps.metadata.services.metadata_value_service import MetadataValueService
from ..exceptions import (
    FileExtensionNotAllowedException,
    FileRequiredException,
    FileSizeExceededException,
)
from ..models import Document


class DocumentService(BaseModelService):
    model = Document
    search_keywords = []
    FILE_SIZE_IN_MB = 500
    FILE_SIZE_IN_KB = FILE_SIZE_IN_MB * 1000
    FILE_SIZE_IN_BYTES = FILE_SIZE_IN_KB * 1000
    FILE_EXTENSIONS = [
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "txt",
        "jpg",
        "jpeg",
        "png",
        "gif",
        "csv",
    ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    @property
    def metadata_value_service(self):
        return MetadataValueService()

    @property
    def category_service(self):
        return CategoryService(user=self.user)

    @property
    def category_permission_service(self):
        return CategoryPermissionService(user=self.user)

    def read_by_uuid(self, uuid_value, **kwargs):
        try:
            instance = super().read_by_uuid(uuid_value, **kwargs)
        except ObjectDoesNotExist:
            raise ObjectNotFoundException("Document not found")
        return instance

    def validate_file_size(self, file):
        if file.size > self.FILE_SIZE_IN_BYTES:
            current_file_size_in_mb = round(file.size / 1000000, 2)
            message = f"File size exceeded {current_file_size_in_mb} MB. Maximum file size allowed is {self.FILE_SIZE_IN_MB} MB"
            raise FileSizeExceededException(message=message)

    def validate_file_extension(self, file):
        extension = Path(file.name).suffix[1:]
        if extension not in self.FILE_EXTENSIONS:
            message = f"File format not allowed. Allowed formats are {', '.join(self.FILE_EXTENSIONS)}."
            raise FileExtensionNotAllowedException(message=message)

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
        self.validate_file_size(kwargs["file"])
        self.validate_file_extension(kwargs["file"])

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

    def generate_response_data(self, instance):
        data = {
            "uuid": instance.uuid,
            "name": instance.name,
            "file": None,
            "extension": "folder",
            "size": None,
            "is_active": instance.is_active,
            "is_encrypted": None,
            "category": None,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "created_by_name": instance.created_by_name,
            "updated_by_name": instance.updated_by_name,
        }

        if isinstance(instance, self.model):
            data.update(
                {
                    "file": instance.file.url,
                    "extension": instance.extension,
                    "size": instance.size,
                    "is_encrypted": instance.is_encrypted,
                    "category": instance.category.code if instance.category else None,
                }
            )
        return data

    def response_list(self, queryset):
        data = []
        for instance in queryset:
            data.append(self.generate_response_data(instance))
        return data

    def search(self, **kwargs):
        category_uuid = kwargs.get("category_uuid")
        viewable_category_codes = list(
            self.category_permission_service.category_code_permissions()
        )

        if viewable_category_codes:
            # if no category requested, return root categories
            if not category_uuid:
                queryset = self.category_service.list(
                    **{
                        "code__in": ",".join(viewable_category_codes),
                        "parent": None,
                        "is_active": True,
                    }
                )
            else:
                kwargs.update(
                    {
                        "category__uuid": category_uuid,
                        "category__code__in": ",".join(viewable_category_codes),
                    }
                )
                queryset = list(self.category_service.list(parent__uuid=category_uuid))
                queryset += self.list(**kwargs)
        else:
            queryset = self.empty_queryset()

        response_data = self.response_list(queryset)
        return response_data
