from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common.utils.basic import get_batch_user

from .services import CategoryPermissionService
from .models import Category


@receiver(post_save, sender=Category)
def create_category_permissions(sender, instance, created, **kwargs):
    if created:
        CategoryPermissionService(user=get_batch_user()).create(instance)
