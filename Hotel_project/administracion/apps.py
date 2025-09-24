from django.apps import AppConfig

class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administracion'

class AdministracionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administracion'

    def ready(self):
        import administracion.signals  # conecta los signals


