from django.apps import AppConfig


class GestorRifaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestor_rifa'
    def ready(self):
        import gestor_rifa.signals

