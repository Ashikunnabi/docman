from apps.common.service import BaseModelService
from apps.common.utils.basic import datetime_now
from apps.category.services.category_service import MenuService

from ..models.menu_item import MenuItem


class MenuItemService(BaseModelService):
    model = MenuItem
    search_keywords = ["menu__name", "item__name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_service = self.get_menu_service()
        self.product_service = self.get_product_service()

    def get_menu_service(self):
        return MenuService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "menu_uuid" in kwargs:
            menu = self.menu_service.read_by_uuid(uuid_value=kwargs["menu_uuid"])
            kwargs["menu_id"] = menu.id
            del kwargs["menu_uuid"]

        if "item_uuid" in kwargs:
            item = self.product_service.read_by_uuid(uuid_value=kwargs["item_uuid"])
            kwargs["item_id"] = item.id
            del kwargs["item_uuid"]

        return kwargs, m2m_data

    def create_menu_item(self, **kwargs):
        remove_keys = []
        for key in remove_keys:
            del kwargs[key]
        kwargs, m2m_data = self.validated_data(**kwargs)
        return self.create(**kwargs)

    def update_menu_item(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance

    def is_active_menu_item(self, menu_item_uuid):
        """
        Check if a menu item is currently active based on various criteria.

        :param menu_item_uuid: The UUID of the menu item to be checked.
        :type menu_item_uuid: str

        :return: True if the menu item is active, False otherwise.
        :rtype: bool
        """
        is_active = True
        menu_item = self.read_by_uuid(uuid_value=menu_item_uuid)

        if not menu_item.is_active:
            is_active = False

        if not menu_item.menu.is_active:
            is_active = False

        if not menu_item.item.is_active:
            is_active = False

        if menu_item.start_at > datetime_now(with_tz=True):
            is_active = False

        if menu_item.end_at < datetime_now(with_tz=True):
            is_active = False

        if menu_item.menu.start_at > datetime_now(with_tz=True):
            is_active = False

        if menu_item.menu.end_at < datetime_now(with_tz=True):
            is_active = False

        return is_active
