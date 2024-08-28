from django.core.management.base import BaseCommand

from apps.category.services.category_permission_service import CategoryPermissionService


class Command(BaseCommand):
    help = "Sync category permissions"

    def handle(self, *args, **options):
        category_permission_service = CategoryPermissionService()
        category_permission_service.sync_category_permissions()
