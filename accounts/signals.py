# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Importar aquí

# accounts/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Metodo

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == 'accounts':
        # Crear nuevos registros en la tabla Metodo
        Metodo.objects.bulk_create([
            Metodo(metodo='NOM-011-STPS-2001'),
            Metodo(metodo='NOM-015-STPS-2001'),
            Metodo(metodo='NOM-022-STPS-2015'),
            Metodo(metodo='NOM-025-STPS-2008'),
            Metodo(metodo='NOM-010-STPS-2014'),
            Metodo(metodo='NOM-081-SEMARNAT-1994'),
        ], ignore_conflicts=True)  # Agregar ignore_conflicts para evitar duplicados
