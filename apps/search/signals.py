# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.category.models.category import Category
from apps.document.models.document import Document
from apps.metadata.models.metadata import Metadata
from apps.metadata.models.metadata_field import MetadataField
from apps.metadata.models.metadata_value import MetadataValue

from apps.search.documents.document_document import DocumentDocument

def get_instance(related_instance):
    if isinstance(related_instance, Category):
        return related_instance.documents.all()
    elif isinstance(related_instance, Metadata):
        return related_instance.categories.documents.all()
    elif isinstance(related_instance, MetadataField):
        return related_instance.metadata.categories.documents.all()
    elif isinstance(related_instance, MetadataValue):
        return Document.objects.filter(id=related_instance.document.id)

@receiver(post_save, sender=Category)
@receiver(post_save, sender=Metadata)
@receiver(post_save, sender=MetadataField)
@receiver(post_save, sender=MetadataValue)
def update_base_document_on_related_change(sender, instance, **kwargs):
    base_instances = get_instance(instance)
    for base_instance in base_instances:
        DocumentDocument().update(base_instance)

@receiver(pre_delete, sender=Category)
@receiver(pre_delete, sender=Metadata)
@receiver(pre_delete, sender=MetadataField)
@receiver(pre_delete, sender=MetadataValue)
def delete_base_document_on_related_delete(sender, instance, **kwargs):
    base_instances = get_instance(instance)
    for base_instance in base_instances:
        DocumentDocument().delete(base_instance)
