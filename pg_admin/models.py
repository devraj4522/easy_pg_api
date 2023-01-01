from django.db import models
from django_extensions.db.models import TimeStampedModel
from shortuuid.django_fields import ShortUUIDField

from easy_pg_backend.users.models import User


class EasyPgUser(TimeStampedModel):
    id = ShortUUIDField(
        length=8,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="easypg_users"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "email",
    ]

    class Meta:
        db_table = "EasyPgUser"

    def __str__(self):
        return self.name if self.name else self.id
