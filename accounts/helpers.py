from .models import Organizacion, Formato

def get_unica_organizacion():
    # Retorna la única organización, asumiendo que solo hay una.
    return Organizacion.objects.first()

def get_formato_default():
    return Formato.objects.first()