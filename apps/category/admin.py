from django.contrib import admin

from apps.common.admin import BaseModelAdmin

from .models import Category, CategoryPermission, CategoryGroupPermission


class CategoryModelAdmin(BaseModelAdmin):
    list_display = ["code", "name", "parent", "is_active"]
    search_fields = ["code", "name"]
    list_filter = ["is_active"]
    ordering = ["code"]
    readonly_fields = ["uuid"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "uuid",
                    "code",
                    "name",
                    "parent",
                    "is_active",
                )
            },
        ),
    )


class CategoryPermissionAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "category"]
    search_fields = ["code", "name"]
    list_filter = ["category"]
    ordering = ["code"]


admin.site.register(Category, CategoryModelAdmin)
admin.site.register(CategoryPermission, CategoryPermissionAdmin)
admin.site.register(CategoryGroupPermission, BaseModelAdmin)
