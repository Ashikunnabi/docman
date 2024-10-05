from apps.common.service import BaseModelService
from apps.document.models.document import Document
from ..documents.document_document import DocumentDocument


class DocumentService(BaseModelService):
    model = Document

    def search(self, **kwargs):
        search_params = kwargs.get("search", "")
        search = DocumentDocument().search()

        # Base query structure
        bool_query = {"bool": {"should": []}}  # Use 'should' for OR logic

        # Add non-nested query
        bool_query["bool"]["should"].append(
            {
                "query_string": {
                    "query": f"*{search_params}*",
                    "fields": ["*"],  # Adjust to specify fields or use ["*"] for all
                    "default_operator": "AND",
                }
            }
        )

        # Add nested query
        bool_query["bool"]["should"].append(
            {
                "nested": {
                    "path": "metadata.fields",  # Replace with your nested path
                    "query": {
                        "query_string": {
                            "query": f"*{search_params}*",
                            "fields": ["*"],  # Specify nested fields
                            "default_operator": "AND",
                        }
                    },
                }
            }
        )

        # Apply the combined bool query to the search
        search = search.query(bool_query)
        queryset = search.to_queryset()
        return queryset
