from django.db import models
from django_extensions.db.models import TimeStampedModel
from shortuuid.django_fields import ShortUUIDField

from easy_pg_backend.users.models import User
from pg_admin.models import EasyPgUser

from .model_helpers import HostelTypeChoice


class CustomersUser(TimeStampedModel):
    id = ShortUUIDField(
        length=8,
        max_length=16,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer_user"
    )
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    active = models.BooleanField(default=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = "customers_users"

    def __str__(self):
        return str(self.name) if self.name else str(self.id)


class Hostel(TimeStampedModel):
    id = ShortUUIDField(
        length=8,
        max_length=16,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        CustomersUser, on_delete=models.CASCADE, related_name="hostels"
    )
    images = models.JSONField(blank=True, null=True, default=dict)
    food_included = models.BooleanField(default=False)

    class Meta:
        db_table = "hostels"

    def __str__(self):
        return self.name if self.name else str(self.id)


class HostelType(TimeStampedModel):
    id = ShortUUIDField(
        length=8,
        max_length=16,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    type = models.CharField(
        max_length=30,
        choices=HostelTypeChoice.choices,
        default=HostelTypeChoice.DOUBLE_SHARING,
    )
    price = models.PositiveIntegerField()
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name="hotel_types"
    )

    class Meta:
        db_table = "hotel_types"

    def __str__(self):
        return self.type if self.type else self.id


class Address(TimeStampedModel):
    id = ShortUUIDField(
        length=8,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=6)
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name="addresses"
    )
    locality = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return str(self.id)


class Review(TimeStampedModel):
    id = ShortUUIDField(
        length=8,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="hostels")
    active = models.BooleanField(default=True)
    images = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return self.title if self.title else str(self.id)
