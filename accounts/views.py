from django.views.generic.list import ListView
from django.utils import timezone
from django.shortcuts import render

from accounts.models import  Notificacion

#   VISTA PARA NOTIFICACIONES DE RECEPCION DE COTIZACIÓN A USUARIO
def notificaciones(request):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    # Por simplicidad, mostraremos un mensaje de notificación estático
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    context={
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
    }
    return render(request, 'accounts/notificaciones/notificaciones.html', context)
