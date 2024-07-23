from datetime import datetime
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import DireccionForm, OrdenTrabajoForm
from accounts.helpers import get_unica_organizacion
from accounts.models import Concepto, Cotizacion, Direccion
from django.contrib import messages
from accounts.forms import OrdenTrabajoForm, DireccionForm
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

# VISTA PRA DIRIGIR A INTERFAZ DE COTIZACIONES ACEPTADAS
def cotizaciones_aceptadas_list(request):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
    # Parámetro de ordenamiento desde la URL
    order_by = request.GET.get('order_by', 'fecha_solicitud')  # Default order
    
    # Filtrar cotizaciones que están aceptadas
    cotizaciones = Cotizacion.objects.filter(estado=True).order_by(order_by)
    
    # Paginación
    paginator = Paginator(cotizaciones, 15) # Mostrar 15 cotizaciones aceptadas por página
    page_number = request.GET.get('page')
    cotizaciones_page = paginator.get_page(page_number)
    
    context = {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'cotizaciones': cotizaciones,
        'cotizaciones_page': cotizaciones_page,  
        
        
    }
    return render(request, "accounts/cotizacionesAceptadas/cotizaciones_aceptadas.html", context)

# VISTA PARA CREAR ORDEN DE TRABAJO
def generar_orden_trabajo(request, pk):
    
    # Obtener la cotización según el ID proporcionado
    cotizacion = get_object_or_404(Cotizacion, id=pk)

    # Verificar que la cotización esté aceptada
    if not cotizacion.estado:
        messages.error(
            request, 'No se puede generar una orden de trabajo para una cotización no aceptada.')
        return redirect('cotizacion_detalle', pk=cotizacion.id)

    # Obtener los conceptos asociados a la cotización
    conceptos = Concepto.objects.filter(cotizacion=cotizacion)

    if request.method == 'POST':
        # Procesar los formularios enviados
        form = OrdenTrabajoForm(request.POST)
        direccion_form = DireccionForm(request.POST)

        if form.is_valid() and direccion_form.is_valid():
            try:
                with transaction.atomic():
                    # Crear una instancia de la orden de trabajo sin guardarla aún
                    orden_trabajo = form.save(commit=False)
                    direccion_data = direccion_form.cleaned_data
                    direccion_actual = cotizacion.persona.empresa.direccion

                    # Verificar si la dirección ha cambiado
                    if not all(direccion_data[key] == getattr(direccion_actual, key) for key in direccion_data):
                        # Crear una nueva dirección si los datos son diferentes
                        nueva_direccion = Direccion.objects.create(
                            **direccion_data)
                        orden_trabajo.direccion = nueva_direccion
                    else:
                        # Usar la dirección actual si los datos no han cambiado
                        orden_trabajo.direccion = cotizacion.persona.empresa.direccion

                    # Verificar si el proyecto es a gestión
                    if 'proyecto_a_gestion' in request.POST:
                        orden_trabajo.gestion = True

                    # Asignar la cotización a la orden de trabajo
                    orden_trabajo.cotizacion = cotizacion
                    orden_trabajo.save()

                    # Filtrar los conceptos seleccionados
                    conceptos_seleccionados = request.POST.getlist('conceptos')
                    for concepto_id in conceptos_seleccionados:
                        concepto = Concepto.objects.get(id=concepto_id)
                        usar_otra_descripcion = request.POST.get(f'usar_otra_descripcion_{concepto_id}')
                        if usar_otra_descripcion:
                            nueva_descripcion = request.POST.get(f'otra_descripcion_{concepto_id}')
                            concepto.notas = nueva_descripcion
                        concepto.save()
                    
                    conceptos_seleccionados = []
                    for concepto in conceptos:
                        if f'usare_concepto_{concepto.id}' in request.POST:
                            descripcion = request.POST.get(f'otra_descripcion_{concepto.id}', concepto.notas)
                            conceptos_seleccionados.append((concepto, descripcion))

                    # Generar el PDF y guardarlo en el modelo
                    pdf_data = generar_pdf_orden_trabajo(request, orden_trabajo, conceptos_seleccionados)
                    orden_trabajo.orden_trabajo_pdf.save(f"orden_trabajo_{orden_trabajo.id_personalizado}.pdf", ContentFile(pdf_data))

                    orden_trabajo.save()

                    messages.success(
                        request, 'Orden de trabajo generada exitosamente.')
                    return redirect('cotizacion_detalle', pk=cotizacion.id)
            except IntegrityError:
                messages.error(
                    request, 'Hubo un error al crear la orden de trabajo. Inténtalo de nuevo.')
        else:
            print(form.errors)
            print(direccion_form.errors)
            messages.error(
                request, 'Hubo un error en el formulario. Por favor, revisa los campos e intenta nuevamente.')
    else:
        direccion_initial_data = {
            'calle': cotizacion.persona.empresa.direccion.calle,
            'numero': cotizacion.persona.empresa.direccion.numero,
            'colonia': cotizacion.persona.empresa.direccion.colonia,
            'ciudad': cotizacion.persona.empresa.direccion.ciudad,
            'codigo': cotizacion.persona.empresa.direccion.codigo,
            'estado': cotizacion.persona.empresa.direccion.estado,
        }
        form = OrdenTrabajoForm()
        direccion_form = DireccionForm(initial=direccion_initial_data)

    context = {
        'form': form,
        'direccion_form': direccion_form,
        'cotizacion': cotizacion,
        'conceptos': conceptos,
    }
    return render(request, 'accounts/cotizacionesAceptadas/generar_orden_trabajo.html', context)

# VISTA PARA CREAR PDF DE ORDEN DE TRABAJO
def generar_pdf_orden_trabajo(request, orden_trabajo, conceptos_seleccionados):
    conceptos = Concepto.objects.filter(cotizacion=orden_trabajo.cotizacion)
    org = get_unica_organizacion()
    formato = org.f_orden.nombre_formato
    version = org.f_orden.version
    emision = org.f_orden.emision
    user = request.user if request.user.is_authenticated else None

    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio

    current_date = datetime.now().strftime("%Y/%m/%d")
    logo_url = request.build_absolute_uri('/static/img/logo.png')

    context = {
        'org': org,
        'formato': formato,
        'version':version,
        'emision':emision,
        'user': user,
        'orden_trabajo': orden_trabajo,
        'conceptos_seleccionados': conceptos_seleccionados,
        'current_date': current_date,
        'logo_url': logo_url,
    }

    html_string = render_to_string(
        'accounts/cotizacionesAceptadas/orden_trabajo_plantilla.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    return pdf
