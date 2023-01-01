from django.contrib import admin

from .models import Address, CustomersUser, Hostel, HostelType, Review

# Register your models here.


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = ("id", "name", "description", "active", "created")
    list_filter = ("active",)
    search_fields = [
        "name",
    ]


@admin.register(HostelType)
class HostelTypeAdmin(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = ("id", "type", "price", "hostel", "created")


@admin.register(CustomersUser)
class CustomersUserAdmin(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = ("id", "name", "phone", "email", "active", "created")
    list_filter = ("active",)
    search_fields = ["name", "email"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = (
        "id",
        "title",
        "description",
        "active",
        "created",
        "hostel",
        "images",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = ("id", "hostel", "city", "state", "pin_code", "locality", "created")
