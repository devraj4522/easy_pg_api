from django.core.exceptions import PermissionDenied
from rest_framework import permissions


class isPgAdmin:
    def has_permission(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Pg_Admin").exists():
            return True
        else:
            raise PermissionDenied("You are not allowed to access this page")
