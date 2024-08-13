import uuid

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
    unsuccessful_attempts = models.IntegerField(null=False, blank=False, default=0)
    history = AuditlogHistoryField()

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
