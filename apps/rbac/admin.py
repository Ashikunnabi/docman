from django.contrib import admin

from apps.rbac.models.branch import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_staff", "is_superuser")


admin.site.register(User, UserAdmin)
