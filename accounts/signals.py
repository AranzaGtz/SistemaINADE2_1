from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Titulo, Metodo

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == 'accounts':
        # Borrar todas las entradas en la tabla Titulo
        Titulo.objects.all().delete()
        
        # Crear nuevos registros en la tabla Titulo
        Titulo.objects.bulk_create([
            Titulo(titulo='Ingeniero', abreviatura='Ing.'),
            Titulo(titulo='Licenciado', abreviatura='Lic.'),
            Titulo(titulo='Arquitecto', abreviatura='Arq.'),
            Titulo(titulo='Contador Público', abreviatura='C.P.'),
            Titulo(titulo='Doctor', abreviatura='Dr.'),
            Titulo(titulo='Maestro', abreviatura='Mtro.'),
            Titulo(titulo='Maestra', abreviatura='Mtra.'),
            Titulo(titulo='Técnico', abreviatura='Téc.'),
            Titulo(titulo='Químico', abreviatura='Quím.'),
            Titulo(titulo='Contador', abreviatura='Cont.'),
            Titulo(titulo='Administrador', abreviatura='Adm.'),
            Titulo(titulo='Abogado', abreviatura='Abog.'),
        ], ignore_conflicts=True)
        
        # Borrar todas las entradas en la tabla Metodo
        
        # Crear nuevos registros en la tabla Metodo
        Metodo.objects.bulk_create([
            Metodo(metodo='NOM-011-STPS-2001'),
            Metodo(metodo='NOM-015-STPS-2001'),
            Metodo(metodo='NOM-022-STPS-2015'),
            Metodo(metodo='NOM-025-STPS-2008'),
            Metodo(metodo='NOM-010-STPS-2014'),
            Metodo(metodo='NOM-081-SEMARNAT-1994'),
        ], ignore_conflicts=True)  # Agregar ignore_conflicts para evitar duplicados
