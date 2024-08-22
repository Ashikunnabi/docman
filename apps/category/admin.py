from django.contrib import admin

from apps.common.admin import BaseModelAdmin

from .models import Category, CategoryPermission, CategoryGroupPermission


class CategoryPermissionAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "category"]
    search_fields = ["code", "name"]
    list_filter = ["category"]
    ordering = ["code"]


# register the Category model with the CategoryAdmin class
admin.site.register(Category, BaseModelAdmin)
admin.site.register(CategoryPermission, CategoryPermissionAdmin)
admin.site.register(CategoryGroupPermission, BaseModelAdmin)
