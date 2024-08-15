#   VISTA PARA OBTENER LA INFORMACION DE LA CONFIGURACIÓN DEL SISTEMA
from accounts.models import ConfiguracionSistema


def obtener_configuracion():
    # Obtiene la primera (y única) instancia de ConfiguracionSistema
    configuracion = ConfiguracionSistema.objects.first()
    return configuracion