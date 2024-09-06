# facturación/context_processors.py

from django.shortcuts import get_object_or_404

from facturacion.models import CSD
from .models import Organizacion


def organization_logo(request):
     org = Organizacion.objects.first()
     return {
          'organization_logo': org.logo.url if org and org.logo else None,
          'organization_name': org.nombre if org and org.nombre else None,
          'organization':org,
     }