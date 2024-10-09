# facturación/context_processors.py

from django.shortcuts import get_object_or_404

from facturacion.models import CSD
from .models import Organizacion

from .models import Notificacion


def notificaciones_no_leidas(request):
     if request.user.is_authenticated:
          notificaciones_no_leidas = Notificacion.objects.filter(
               usuario=request.user, leido=False).count()
     else:
          notificaciones_no_leidas = 0
     return {
          'notificaciones_no_leidas': notificaciones_no_leidas
     }


def organization_logo(request):
     org = Organizacion.objects.first()
     return {
          'organization_logo': org.logo.url if org and org.logo else None,
          'organization_name': org.nombre if org and org.nombre else None,
          'organization': org,
     }
