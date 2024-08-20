# VISTA PARA MODIFICAR NUESTRA INFORMACION DE FORMATO
from datetime import datetime, timedelta
import os
import random
from django.http import HttpResponse
from django.shortcuts import  redirect, render
from accounts.forms import FormatoCotizacionForm, FormatoOrdenForm, OrganizacionForm, QuejaForm
from accounts.helpers import get_unica_organizacion
from accounts.models import  Concepto, Cotizacion, Empresa, FormatoCotizacion, FormatoOrden, Organizacion, Persona, Servicio, Titulo
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings

from weasyprint import HTML  # type: ignore

#   VISTA PARA ACTUALIZAR LA ORGANIZACIÓN
def editar_organizacion(request):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    organizacion = Organizacion.objects.first() # Asume que solo hay una organización
    
    if not organizacion:
        # Si no existe ninguna organización, crea una nueva instancia
        organizacion = Organizacion()
        organizacion.save()

    if request.method == 'POST':
        form = OrganizacionForm(request.POST,request.FILES, instance=organizacion)
        # Verifica si el logo ha cambiado
        if 'logo' in form.changed_data:
            if organizacion.logo:
                # Borra el logo antiguo si existe
                if os.path.isfile(organizacion.logo.path):
                    os.remove(organizacion.logo.path)
        form.save()
        messages.success(request, 'Organización actualizada correctamente!.')
        return redirect('editar_organizacion')  # Redirige a la página actual

    else:
        form = OrganizacionForm(instance=organizacion)
    context={
        'form':form,
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'organizacion':organizacion
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
            formato_cotizacion_form = FormatoCotizacionForm(request.POST,request.FILES, instance=formato_cotizacion)
            if formato_cotizacion_form.is_valid():
                formato_cotizacion_form.save()
                messages.success(request, 'Formato de cotización actualizado correctamente!.')
                return redirect('home')  # Asumiendo que 'home' es la URL de redirección
        elif 'guardar_orden' in request.POST:
            formato_orden_form = FormatoOrdenForm(request.POST,request.FILES, instance=formato_orden)
            if formato_orden_form.is_valid():
                formato_orden_form.save()
                messages.success(request, 'Formato de orden de trabajo actualizado correctamente!.')
                return redirect('home')

    context = {
        'formato_cotizacion_form': formato_cotizacion_form,
        'formato_orden_form': formato_orden_form,
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'formato_cotizacion': formato_cotizacion,
        'formato_orden': formato_orden,
    }

    return render(request, 'accounts/organizacion/formatos.html', context)

# VISTA PARA QUEJAS
def enviar_queja(request):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
    if request.method == 'POST':
        form = QuejaForm(request.POST, request.FILES)
        if form.is_valid():
            queja = form.save(commit=False)
            queja.nombre = request.user.first_name
            queja.email = request.user.email
            queja.save()
            send_mail(
                subject=f"Nuevo Queja: {queja.asunto}",
                message=f"Nombre: {queja.nombre}\nEmail: {queja.email}\nAsunto: {queja.asunto}\nMensaje: {queja.mensaje}\nPrioridad: {queja.prioridad}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.SUPPORT_EMAIL],
            )
            messages.success(request, 'Solicitud de queja enviada con éxito!')
            return redirect('home')
    else:
        form = QuejaForm()
        
    context = {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'form': form
    }
    return render(request, 'accounts/organizacion/enviar_queja.html', context)

def cotizacion_prueba(request):
    # Obtener el número total de cotizaciones en la base de datos
    total_cotizaciones = Cotizacion.objects.count()

    # Verificar que haya al menos una cotización
    if total_cotizaciones > 0:
        # Elegir un índice aleatorio
        random_index = random.randint(0, total_cotizaciones - 1)
        
        # Obtener una cotización aleatoria
        cotizacion = Cotizacion.objects.all()[random_index]
        conceptos = cotizacion.conceptos.all()
        org = get_unica_organizacion()
        formato = org.f_cotizacion
        user = request.user if request.user.is_authenticated else None
        
        for concepto in conceptos:
            concepto.subtotal = concepto.cantidad_servicios * concepto.precio
        
        current_date = datetime.now().strftime("%Y/%m/%d")
        logo_url = request.build_absolute_uri('/static/img/logo.png')
        marca = request.build_absolute_uri('/static/img/Imagen 21.jpg')

        context = {
            'org': org,
            'org_form': formato,
            'user': user,
            'cotizacion': cotizacion,
            'conceptos': conceptos,
            'current_date': current_date,
            'logo_url': logo_url,
            'marca': marca,
        }

        html_string = render_to_string('accounts/cotizaciones/cotizacion_platilla.html', context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        # Crear una respuesta HTTP con el PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cotizacion_aleatoria.pdf"'
        return response
    else:
        return HttpResponse("No hay cotizaciones disponibles.")
        
    
    