from django.shortcuts import get_object_or_404, render
from accounts.models import OrdenTrabajo

# Create your views here.
#    VISTA DE FORMULARIO DE CREACIÓN DE FACTURA
def crear_factura(request, id_personalizado):
     orden = get_object_or_404(OrdenTrabajo, id_personalizado = id_personalizado)
     context = {
          'orden': orden
     }
     return render(request,'facturacion/formulario.html',context)


#    VISTA DE LISTA DE FACTURAS