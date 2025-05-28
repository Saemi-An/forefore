from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.products'

    def ready(self):
        import core.products.signals  # noqa: F401
