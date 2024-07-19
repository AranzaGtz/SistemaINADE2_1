from django.http import JsonResponse
from django.views.generic.list import ListView
from django.utils import timezone
from django.shortcuts import get_object_or_404, render

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

#   VISTA PARA HACER QUE LA NOTIFICACIÓN CAMBIE A LEIDA
def marcar_notificacion_leida(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk)
    notificacion.leido = True
    notificacion.save()
    return JsonResponse({'success': True})

#   VISTA PARA BORRAR NOTIFICACIONES
def borrar_notificacion(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk)
    notificacion.delete()
    return JsonResponse({'success': True})