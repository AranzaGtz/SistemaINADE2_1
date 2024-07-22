from .models import FormatoCotizacion, Organizacion

def get_unica_organizacion():
    # Retorna la única organización, asumiendo que solo hay una.
    return Organizacion.objects.first()

def get_formato_default():
    return FormatoCotizacion.objects.first()