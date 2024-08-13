from apps.common.models import BaseModel
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.db import models



User = get_user_model()


class Branch(BaseModel):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex="[-a-zA-Z0-9_.\s]{2,100}$",
                message="Branch contains alphanumeric, "
                "underscore, space and period(.). "
                "Length: 2 to 100",
            )
        ],
    )
    parent = models.ForeignKey(
        "self",
        blank=True,
        related_name="subbranches",
        null=True,
        on_delete=models.CASCADE,
    )
    user = models.ManyToManyField(User, blank=True, related_name="branchs")
    group = models.ManyToManyField(Group, blank=True, related_name="branchs")
    address = models.TextField(blank=True)

    def get_users(self):
        # this will return all users id from user and group field
        user_id = self.user.values_list("id", flat=True)
        all_user = [(user_id + g.user.values_list("id", flat=True)) for g in self.group]
        return list(dict.fromkeys(all_user[0]))  # all unique user list

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ("name", "parent")
        ordering = ("name",)
