from django.shortcuts import render
from accounts.models import OrdenTrabajo

#    VISTA PARA ORDENES DE TRABAJO
def ordenes_list(request):
     ordenes = OrdenTrabajo.objects.filter(estado=False)
     return render(request, 'accounts/ordenes/ordenes.html', {'ordenes': ordenes})