from apps.category.models.category import Category
from apps.document.models.document import Document as Doc
from apps.metadata.models.metadata import Metadata
from apps.metadata.models.metadata_field import MetadataField
from apps.metadata.models.metadata_value import MetadataValue
from django_elasticsearch_dsl import Document as Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class DocumentDocument(Document):
    name = fields.TextField()

    category = fields.ObjectField(
        properties={
            "uuid": fields.KeywordField(),
            "name": fields.TextField(),
            "code": fields.KeywordField(),
            "parent": fields.KeywordField(),
        }
    )

    metadata = fields.NestedField(
        properties={
            "uuid": fields.KeywordField(),
            "name": fields.TextField(),
            "fields": fields.NestedField(
                properties={
                    "uuid": fields.KeywordField(),
                    "name": fields.TextField(),
                    "value": fields.TextField(),
                }
            ),
        }
    )
    created_by_name = fields.TextField()
    updated_by_name = fields.TextField()

    def prepare_category(self, instance):
        if not instance.category:
            return None

        return {
            "uuid": str(instance.category.uuid),
            "name": instance.category.name,
            "code": instance.category.code,
            "parent": (
                str(instance.category.parent.uuid) if instance.category.parent else None
            ),
        }

    def prepare_metadata(self, instance):
        if not instance.category:
            return None

        data = [
            {
                "uuid": str(metadata.uuid),
                "name": metadata.name,
                "fields": [
                    {
                        "uuid": str(field.uuid),
                        "name": field.name,
                        "value": (
                            str(field.values.get(document=instance).get_value())
                            if field.values.filter(document=instance).exists()
                            else ""
                        ),
                    }
                    for field in metadata.fields.all()
                ],
            }
            for metadata in instance.category.metadata.all()
        ]

        return data

    def prepare_created_by_name(self, instance):
        return instance.created_by_name

    def prepare_updated_by_name(self, instance):
        return instance.updated_by_name

    class Index:
        name = "document"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Doc
        fields = [
            "uuid",
            "extension",
            "size",
            "is_active",
            "is_encrypted",
            "created_at",
            "updated_at",
        ]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("category")
            .prefetch_related("category__metadata__fields__values")
        )
