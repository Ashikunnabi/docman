from apps.common.admin import BaseModelAdmin
from .models import Document
from django.contrib import admin


class DocumentAdmin(BaseModelAdmin):
    model = Document

admin.site.register(Document, DocumentAdmin)
