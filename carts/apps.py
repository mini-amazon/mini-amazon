from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carts'
    verbose_name = _('Shopping Carts')

    def ready(self):
        # Import signal handlers
        import carts.signals
