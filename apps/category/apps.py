from django.apps import AppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.category'

    def ready(self):
        import apps.category.signals
