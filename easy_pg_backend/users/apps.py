from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "easy_pg_backend.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import easy_pg_backend.users.signals  # noqa F401
        except ImportError:
            pass
