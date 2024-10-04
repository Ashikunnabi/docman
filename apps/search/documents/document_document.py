from apps.document.models.document import Document
from django_elasticsearch_dsl import Document as EsDocument, fields
from django.elasticsearch_dsl.registries import registry


class DocumentDocument(EsDocument):
    class Index:
        name = "document"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        category = fields.ObjectField(properties={
            "uuid": fields.KeywordField(),
            "name": fields.TextField(),
            "code": fields.KeywordField(),
            "parent": fields.IntegerField(),
        })
        model = Document
        fields = [
            "uuid",
            "name",
            "file",
            "extension",
            "size",
            "is_active",
            "is_encrypted",
            "category",
            "created_at",
            "updated_at",
            "created_by_name",
            "updated_by_name",
        ]

