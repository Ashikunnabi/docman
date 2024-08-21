from django.contrib import admin

from .models import Category, CategoryPermission, CategoryGroupPermission


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    search_fields = ["name"]
    list_filter = ["parent"]
    ordering = ["name"]


class CategoryPermissionAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "category"]
    search_fields = ["code", "name"]
    list_filter = ["category"]
    ordering = ["code"]

class CategoryGroupPermissionAdmin(admin.ModelAdmin):
    list_display = ["group", "permission"]
    search_fields = ["group", "permission"]
    list_filter = ["group", "permission"]
    ordering = ["group", "permission"]


# register the Category model with the CategoryAdmin class
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryPermission, CategoryPermissionAdmin)
admin.site.register(CategoryGroupPermission, CategoryGroupPermissionAdmin)
