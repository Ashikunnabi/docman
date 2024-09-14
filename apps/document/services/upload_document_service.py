import time
from pathlib import Path

import qrcode
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from apps.common.service import BaseModelService
from .document_service import DocumentService


class UploadDocumentService(BaseModelService):
    model = None

    def __init__(self, data=None, file_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.file_path = file_path

    @property
    def document_service(self):
        return DocumentService(user=self.user)

    def save_file_in_storage(self, file):
        file_name = file.name
        file_content = file

        if (isinstance(file, InMemoryUploadedFile) or
            isinstance(file, TemporaryUploadedFile)
        ):
            file_name = file.name
            file_content = file_content.read()

        file_path = f"{self.file_path}{file_name}"

        # save file into Default Storage
        final_path = default_storage.save(file_path, ContentFile(file_content))

        # save data into Document model
        document = self.document_service.create_document(**{"path": final_path})
        return document
