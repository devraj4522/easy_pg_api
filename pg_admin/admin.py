from django.contrib import admin

from .models import EasyPgUser

# Register your models here.


@admin.register(EasyPgUser)
class EasyPgUserAdmin(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = ("id", "name", "email", "active", "created")
    list_filter = ("active",)
    search_fields = ["name", "email"]
