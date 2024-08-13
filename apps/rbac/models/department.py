from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.db import models

from apps.common.models import BaseModel
from .branch import Branch

User = get_user_model()


class Department(BaseModel):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex="[-a-zA-Z0-9_.\s]{2,100}$",
                message="Department contains alphanumeric, "
                "underscore, space and period(.). "
                "Length: 2 to 100",
            )
        ],
    )
    branch = models.ForeignKey(
        Branch, related_name="departments", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "self",
        related_name="subdepartments",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    user = models.ManyToManyField(User, blank=True, related_name="departments")
    group = models.ManyToManyField(Group, blank=True, related_name="departments")

    def get_users(self):
        # this will return all users id from user and group field
        user_id = self.user.values_list("id", flat=True)
        all_user = [(user_id + g.user.values_list("id", flat=True)) for g in self.group]
        return list(dict.fromkeys(all_user[0]))  # all unique user list

    def __str__(self):
        return f"{self.name} ({self.branch.name})"
