from apps.common.service import BaseModelService
from apps.document.services.upload_document_service import UploadDocumentService
from apps.menu.services.menu_document_service import MenuDocumentService

from ..models.menu import Menu


class MenuService(BaseModelService):
    model = Menu
    search_keywords = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_type_service = self.get_menu_type_service()

    def get_menu_type_service(self):
        from apps.menu.services import MenuTypeService

        return MenuTypeService()

    def get_upload_document_service(self, file_path):
        return UploadDocumentService(file_path=file_path)

    def get_menu_document_service(self):
        return MenuDocumentService()

    def get_menu_type(self, uuid):
        menu_type = self.menu_type_service.read_by_uuid(uuid_value=uuid)
        return menu_type

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "type_uuid" in kwargs:
            kwargs["type_id"] = self.get_menu_type(uuid=kwargs["type_uuid"]).id
            del kwargs["type_uuid"]

        return kwargs, m2m_data

    def create_menu(self, **kwargs):
        remove_keys = []
        for key in remove_keys:
            del kwargs[key]
        kwargs, m2m_data = self.validated_data(**kwargs)
        return self.create(**kwargs)

    def update_menu(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance



    def upload_document(self, *args, **kwargs):
        menu_uuid = kwargs["menu_uuid"]
        menu = self.read_by_uuid(uuid_value=menu_uuid)
        file_path = f"menus/{menu_uuid}/"

        upload_document_service = self.get_upload_document_service(file_path=file_path)
        menu_document_service = self.get_menu_document_service()
        document = upload_document_service.save_file_in_storage(file=kwargs["file"])

        # save data into ProductDocument model
        menu_document_data = {
            "menu_id": menu.id,
            "document_id": document.id,
            "sort_order": kwargs.get("sort_order", 0),
        }
        menu_document = menu_document_service.create_menu_document(
            **menu_document_data
        )

        return menu_document
