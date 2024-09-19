# VISTA PARA MODIFICAR NUESTRA INFORMACION DE FORMATO
from datetime import datetime, timedelta
import os
import random
from django.http import HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from accounts.forms import AlmacenForm, ConfiguracionSistemaForm, DireccionForm, FormatoCotizacionForm, FormatoOrdenForm, OrganizacionForm, QuejaForm, SucursalForm
from accounts.helpers import get_unica_organizacion
from accounts.models import  Concepto, ConfiguracionSistema, Cotizacion, CustomUser, Direccion, Empresa, FormatoCotizacion, FormatoOrden, Organizacion, Persona, Servicio, Titulo
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings

from weasyprint import HTML  # type: ignore

#   VISTA PARA LA INTERFAZ DE FORMATOS
def formatos(request):
    # Notificaciones del usuario
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
    organizacion = request.user.organizacion
    org_direccion = organizacion.direccion
    
    formato_cotizacion = organizacion.f_cotizacion
    formato_orden = organizacion.f_orden
    
    # Verificar si la organización tiene una dirección
    if not org_direccion:
        # Crear una dirección vacía y asignarla a la organización
        org_direccion = Direccion(
            calle='',
            numero='',
            colonia='',
            ciudad='',
            codigo='',
            estado=''
        )
        org_direccion.save()
        organizacion.direccion = org_direccion
        organizacion.save()
    
    # Inicializar formularios con las instancias existentes
    formato_cotizacion_form = FormatoCotizacionForm(instance=formato_cotizacion)
    formato_orden_form = FormatoOrdenForm(instance=formato_orden)
    
    # Inicializar el formulario de organización con la instancia
    organizacion_form = OrganizacionForm(instance=organizacion)
    
    if org_direccion:
        organizacion_form.fields['calle'].initial = org_direccion.calle
        organizacion_form.fields['numero'].initial = org_direccion.numero
        organizacion_form.fields['colonia'].initial = org_direccion.colonia
        organizacion_form.fields['ciudad'].initial = org_direccion.ciudad
        organizacion_form.fields['codigo'].initial = org_direccion.codigo
        organizacion_form.fields['estado'].initial = org_direccion.estado
    
    # Obtén la primera instancia de ConfiguracionSistema o crea una si no existe
    configuracion, created = ConfiguracionSistema.objects.get_or_create(id=1)
    
    # Inicializar la variable forms
    forms = ConfiguracionSistemaForm(instance=configuracion)
    
    # Si el formulario es POST, manejar la actualización
    if request.method == 'POST':
        if 'guardar_cotizacion' in request.POST:
            formato_cotizacion_form = FormatoCotizacionForm(request.POST, request.FILES, instance=formato_cotizacion)
            if formato_cotizacion_form.is_valid():
                formato_cotizacion_form.save()
                messages.success(request, 'Formato de cotización actualizado correctamente!.')
                return redirect('home')
        elif 'guardar_orden' in request.POST:
            formato_orden_form = FormatoOrdenForm(request.POST, request.FILES, instance=formato_orden)
            if formato_orden_form.is_valid():
                formato_orden_form.save()
                messages.success(request, 'Formato de orden de trabajo actualizado correctamente!.')
                return redirect('home')
        elif 'guardar_organizacion' in request.POST:
            organizacion_form = OrganizacionForm(request.POST, request.FILES, instance=organizacion)
            if organizacion_form.is_valid():
                organizacion_form.save()
                # Actualizar la dirección existente
                org_direccion.calle = request.POST.get('calle')
                org_direccion.numero = request.POST.get('numero')
                org_direccion.colonia = request.POST.get('colonia')
                org_direccion.ciudad = request.POST.get('ciudad')
                org_direccion.codigo = request.POST.get('codigo')
                org_direccion.estado = request.POST.get('estado')
                org_direccion.save()
                messages.success(request, 'Organización y dirección actualizadas correctamente!.')
                return redirect('home')
        elif 'guardar_sistema' in request.POST:
            forms = ConfiguracionSistemaForm(request.POST, instance=configuracion)
            if forms.is_valid():
                forms.save()
                messages.success(request, 'La configuración del sistema se ha actualizado correctamente.')
                return redirect('home')
    
    context = {
        'formato_cotizacion_form': formato_cotizacion_form,
        'formato_orden_form': formato_orden_form,
        'form': organizacion_form,
        'forms': forms,
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'formato_cotizacion': formato_cotizacion,
        'formato_orden': formato_orden,
        'organizacion': organizacion,
    }

    return render(request, 'accounts/organizacion/formatos.html', context)


#   VISTA PARA QUEJAS
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

#   VISTA PARA PROBAR COTIZACIÓN
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
        
#   VISTA PARA CREAR SUCURSAL
def sucursal(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        direccion_form = DireccionForm(request.POST)

        organizacion = get_object_or_404(Organizacion, pk=1)

        if form.is_valid() and direccion_form.is_valid():
            direccion = direccion_form.save()  # Guarda la dirección

            sucursal = form.save(commit=False)
            sucursal.organizacion = organizacion
            sucursal.direccion = direccion  # Asigna la dirección a la sucursal
            sucursal.save()
            messages.success(request, 'Se agrego correctamente la sucursal.')
            return redirect('sucursal')
    else:
        form = SucursalForm()
        direccion_form = DireccionForm()

    context = {
        'form': form,
        'direccion_form': direccion_form,
    }
    return render(request, 'accounts/organizacion/sucursal.html', context)

#   VISTA PARA CREAR SUCURSAL
def almacen(request):
    if request.method == 'POST':
        almacenForm = AlmacenForm(request.POST)
        direccion_form = DireccionForm(request.POST)

        organizacion = get_object_or_404(Organizacion, pk=1)

        if almacenForm.is_valid() and direccion_form.is_valid():
            direccion = direccion_form.save()  # Guarda la dirección

            almacen = almacenForm.save(commit=False)
            almacen.organizacion = organizacion
            almacen.direccion = direccion  # Asigna la dirección al almacén
            almacen.save()
            messages.success(request,'Se agrego correctamente el almacen.')
            return redirect('almacen')
    else:
        almacenForm = AlmacenForm()
        direccion_form = DireccionForm()

    context = {
        'almacenForm': almacenForm,
        'direccion_form': direccion_form,
    }
    return render(request, 'accounts/organizacion/alamacen.html', context)
    