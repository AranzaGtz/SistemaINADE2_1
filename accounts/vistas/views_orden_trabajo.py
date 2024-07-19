from django.shortcuts import render
from accounts.models import OrdenTrabajo

#    VISTA PARA ORDENES DE TRABAJO
def ordenes_list(request):
     # Notificación
     notificaciones = request.user.notificacion_set.all()
     notificaciones_no_leidas = notificaciones.filter(leido=False).count()

     ordenes = OrdenTrabajo.objects.filter(estado=False)
     context={
          'notificaciones': notificaciones,
          'notificaciones_no_leidas': notificaciones_no_leidas,
          'ordenes':ordenes
     }
     return render(request, 'accounts/ordenes/ordenes.html', {'ordenes': ordenes})