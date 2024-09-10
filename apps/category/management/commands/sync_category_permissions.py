from django.core.management.base import BaseCommand

from apps.category.services.category_permission_service import CategoryPermissionService
from apps.common.utils.basic import get_batch_user


class Command(BaseCommand):
    help = "Sync category permissions"

    def handle(self, *args, **options):
        category_permission_service = CategoryPermissionService(user=get_batch_user())
        category_permission_service.sync_category_permissions()
