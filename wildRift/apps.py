from django.apps import AppConfig


class WildriftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wildRift'

    def ready(self):
        import wildRift.signals