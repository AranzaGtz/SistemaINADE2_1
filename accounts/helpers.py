from .models import Organizacion, Formato

def get_unica_organizacion():
    # Retorna la única organización, asumiendo que solo hay una.
    return Organizacion.objects.first()

def get_formato_default(organizacion):
    # Retorna el primer formato relacionado con la organización o None si no existe ninguno.
    return organizacion.formatos.first()
