from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import CategoryPermissionService
from .models import Category


@receiver(post_save, sender=Category)
def create_category_permissions(sender, instance, created, **kwargs):
    if created:
        CategoryPermissionService().create(instance)
