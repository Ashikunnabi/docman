import uuid

from apps.category.models.category_group_permission import CategoryGroupPermission
from apps.category.models.category_permission import CategoryPermission
from auditlog.models import AuditlogHistoryField
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        db_index=True,
        help_text="This will be exposed to the outside world.",
    )
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=15, null=True, blank=True)

    is_password_change_required = models.BooleanField(
        null=False, blank=False, default=False
    )
    password_updated_at = models.DateTimeField(null=True, blank=True)
    is_user_locked = models.BooleanField(null=False, blank=False, default=False)
    user_locked_at = models.DateTimeField(null=True, blank=True)
    last_unsuccessful_login = models.DateTimeField(null=True, blank=True)
    unsuccessful_login_attempts = models.IntegerField(
        null=False, blank=False, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def get_category_permissions(self):
        """List of category permission codes for the user."""
        # superuser has all permissions by default and can access all categories
        # users with create_category permission can access all categories
        if self.has_perm("category.create_category"):
            return CategoryPermission.objects.values_list("code", flat=True).distinct()

        permission_codes = (
            CategoryGroupPermission.objects.filter(group__in=self.groups.all())
            .values_list("permission__code", flat=True)
            .distinct()
        )
        return list(permission_codes)

    def has_category_permission(self, permission_code):
        return permission_code in self.get_category_permissions()

    def get_permitted_category_uuids(self):
        category_uuids = (
            CategoryGroupPermission.objects.filter(group__in=self.groups.all())
            .values_list("permission__category__uuid", flat=True)
            .distinct()
            .prefetch_related("category")
        )
        return list(category_uuids)
