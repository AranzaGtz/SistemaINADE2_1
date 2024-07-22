# VISTA PARA MODIFICAR NUESTRA INFORMACION DE FORMATO
from django.shortcuts import  redirect, render
from accounts.forms import FormatoCotizacionForm, FormatoOrdenForm, OrganizacionForm
from accounts.models import  FormatoCotizacion, FormatoOrden, Organizacion
from django.contrib import messages

#   VISTA PARA ACTUALIZAR LA ORGANIZACIÓN
def editar_organizacion(request):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    organizacion = Organizacion.objects.first()
    if not organizacion:
        # Si no existe ninguna organización, crea una nueva instancia
        organizacion = Organizacion()
        organizacion.save()

    if request.method == 'POST':
        form = OrganizacionForm(request.POST, instance=organizacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organización actualizada correctamente!.')
            return redirect('home')  # Redirige a la página de inicio o a la página adecuada
    else:
        form = OrganizacionForm(instance=organizacion)
    context={
        'form':form,
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
    }
    return render(request, 'accounts/organizacion/editar_organizacion.html',context)

#   VISTA PARA LA INTERFAZ DE FORMATOS
def formatos(request):
    # Notificaciones del usuario
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
    # Obtener el primer registro o none
    formato_cotizacion = FormatoCotizacion.objects.first()
    formato_orden = FormatoOrden.objects.first()

    # Inicializar formularios con la instancia existente o nueva si no hay registro
    formato_cotizacion_form = FormatoCotizacionForm(instance=formato_cotizacion)
    formato_orden_form = FormatoOrdenForm(instance=formato_orden)
    
    if request.method == 'POST':
        if 'guardar_cotizacion' in request.POST:
            formato_cotizacion_form = FormatoCotizacionForm(request.POST, instance=formato_cotizacion)
            if formato_cotizacion_form.is_valid():
                formato_cotizacion_form.save()
                messages.success(request, 'Formato de cotización actualizado correctamente!.')
                return redirect('home')  # Asumiendo que 'home' es la URL de redirección
        elif 'guardar_orden' in request.POST:
            formato_orden_form = FormatoOrdenForm(request.POST, instance=formato_orden)
            if formato_orden_form.is_valid():
                formato_orden_form.save()
                messages.success(request, 'Formato de orden de trabajo actualizado correctamente!.')
                return redirect('home')

    context = {
        'formato_cotizacion_form': formato_cotizacion_form,
        'formato_orden_form': formato_orden_form,
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
    }

    return render(request, 'accounts/organizacion/formatos.html', context)