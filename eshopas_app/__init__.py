from django.apps import AppConfig

class EshopasAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eshopas_app'

    def ready(self):
        import eshopas_app.templatetags.custom_filters