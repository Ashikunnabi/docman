import datetime
import re
import uuid

from auditlog.models import AuditlogHistoryField
from django.db import models


class BaseModel(models.Model):
    validators = []

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        db_index=True,
        help_text="This will be exposed to the outside world.",
    )
    created_by = models.ForeignKey(
        "rbac.user",
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "rbac.user",
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(default=True)
    history = AuditlogHistoryField()

    class Meta:
        abstract = True

    def get_validators(self):
        """Returns list of validators"""
        return self.validators

    def get_screen_methods(self):
        """Returns list of all methods whose name starts with 'screen_'"""

        screen_methods = []
        attributes = dir(self)
        pattern = re.compile("screen[_]*")
        for attribute in attributes:
            if pattern.match(attribute):
                screen_methods.append(getattr(self, attribute))
        return screen_methods

    def check_validators(self):
        """Pass the object to all validators for validation"""

        validators = self.get_validators()
        for validator in validators:
            validator(obj=self).validate()

    def clean(self, *args, **kwargs):
        super().clean()
        self.check_validators()

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:
            # Only set added_by during the first save.
            try:
                # exposed_request comes from RequestExposerMiddleware
                self.created_by = exposed_request.user
            except Exception:
                self.created_by_id = 1  # Request from management command
            self.updated_by = self.created_by
        else:
            try:
                self.updated_by = exposed_request.user
            except Exception:
                self.updated_by_id = 1  # Request from management command

            if self.is_soft_deleted:
                self.soft_deleted_at = datetime.datetime.now()
        super().save(*args, **kwargs)

    @property
    def created_by_name(self):
        return (
            f"{self.created_by.name} ({self.created_by.username})"
            if self.created_by
            else ""
        )

    @property
    def updated_by_name(self):
        return (
            f"{self.updated_by.name} ({self.updated_by.username})"
            if self.updated_by
            else ""
        )
