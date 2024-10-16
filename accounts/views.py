from django.http import JsonResponse
from django.views.generic.list import ListView
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import ConfiguracionSistemaForm
from accounts.models import  ConfiguracionSistema, Notificacion, Organizacion
from .utils import obtener_configuracion
from django.contrib import messages


#   VISTA PARA IR A LA CONFIGURACIÓN DEL SISTEMA
def editar_configuracion_sistema(request):
    # Obtén la organización del usuario logueado
    organizacion = get_object_or_404(Organizacion, id=request.user.organizacion.id)  # Suponiendo que tienes una relación en el usuario
    configuracion = organizacion.configuracion_sistema

    if request.method == 'POST':
        form = ConfiguracionSistemaForm(request.POST, instance=configuracion)
        if form.is_valid():
            form.save()
            messages.success(request, 'La configuración del sistema se ha actualizado correctamente.')
            return redirect('editar_configuracion_sistema')  # Redirige a la misma página o a otra
    else:
        form = ConfiguracionSistemaForm(instance=configuracion)
    
    return render(request, 'accounts/sistema/editar_configuracion_sistema.html', {'form': form})

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

