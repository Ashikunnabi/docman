from django.contrib import admin

# Register your models here.

from .models import Metadata, MetadataField

admin.site.register(Metadata)
admin.site.register(MetadataField)