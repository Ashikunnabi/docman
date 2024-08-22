from django.contrib import admin
from django.db import models


class BaseModelAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.autocomplete_fields = self._get_autocomplete_fields()

    def _get_autocomplete_fields(self):
        autocomplete_fields = []
        for field in self.model._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                autocomplete_fields.append(field.name)
        return autocomplete_fields

    list_display = [
        "uuid",
        "is_active",
        "created_at",
        "updated_at",
        "created_by_name",
        "updated_by_name",
    ]
    search_fields = [
        "uuid",
        "is_active",
        "created_at",
        "updated_at",
        "created_by_name",
        "updated_by_name",
    ]
    readonly_fields = [
        "uuid",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    ]
    list_filter = ["is_active", "created_at", "updated_at"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
