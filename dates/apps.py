from django.apps import AppConfig


class DatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dates'

    def ready(self):
        import dates.signals
