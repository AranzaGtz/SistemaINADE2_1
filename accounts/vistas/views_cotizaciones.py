from datetime import datetime
from decimal import Decimal
import json
from django.db import IntegrityError
from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from accounts.helpers import  get_unica_organizacion
from accounts.models import Cotizacion, Concepto, Empresa, InformacionContacto, Metodo, OrdenTrabajo, Persona, Prospecto, Servicio, Titulo
from accounts.forms import ConceptoForm, CotizacionForm, CotizacionChangeForm, ConceptoFormSet, DireccionForm, EmpresaForm, MetodoForm, PersonaForm, ProspectoForm, ServicioForm, ServicioForm2
from django.contrib import messages
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from weasyprint import HTML  # type: ignore
from django.template.loader import render_to_string
from django.db import IntegrityError, transaction
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

# VISTA PARA AGREGAR UN SERVICIO
def agregar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm2(request.POST)
        if form.is_valid():
            servicio = form.save()
            # Devuelve un script para cerrar la ventana y actualizar el campo select
            return HttpResponse(f"""
                <script>
                    window.opener.actualizarSelectServicio({{ id: {servicio.id}, nombre: '{servicio.nombre_servicio}' }});
                    window.close();
                </script>
            """)
    else:
        form = ServicioForm2()

    return render(request, 'accounts/servicios/agregar_servicio.html', {'form': form})

# VISTA PARA GENERAD ID PERSONALIZADO
def generate_new_id_personalizado():
    last_cotizacion = Cotizacion.objects.order_by('id_personalizado').last()
    if not last_cotizacion:
        return '0001'
    last_id = last_cotizacion.id_personalizado
    new_id = int(last_id) + 1
    return str(new_id).zfill(4)

# VISTA DE COTIZACIONES
def cotizaciones_list(request):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
    # Parámetro de ordenamiento desde la URL
    order_by = request.GET.get('order_by', 'id')  # Default order
    
    if not order_by:  # Asegura que siempre haya un valor válido para order_by
        order_by = 'id'

    # Filtrar cotizaciones que no están aceptadas y ordenarlas
    cotizaciones = Cotizacion.objects.all().order_by(order_by)
    
    # Paginación
    paginator = Paginator(cotizaciones, 50)  # Mostrar 50 cotizaciones por página
    page_number = request.GET.get('page')
    cotizaciones_page = paginator.get_page(page_number)

    context = {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'cotizaciones_page': cotizaciones_page,  # Cambiado a cotizaciones_page
        'cotizaciones':cotizaciones,
    }
    return render(request, "accounts/cotizaciones/cotizaciones.html", context)

# VISTA PARA OBTENER INFORMACION DEL CLIENTE HE IMPRMIR EN FORMULARIO
def obtener_datos_cliente(request, cliente_id):
    persona = Persona.objects.filter(id=cliente_id).select_related(
        'informacion_contacto', 'empresa').first()
    if persona:
        data = {
            'nombre': persona.nombre,
            'correo': persona.informacion_contacto.correo_electronico if persona.informacion_contacto else 'No disponible',
            'telefono': persona.informacion_contacto.celular,
            'rfc': persona.empresa.rfc,
            'empresa': persona.empresa.nombre_empresa if persona.empresa else 'No disponible',

            # Agrega otros campos que necesites
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

# VISTA PARA OBTENER INFORMACION DEL SERVICIO HE IMPRMIR EN FORMULARIO
def obtener_datos_servicio(request, servicio_id):
    servicio = Servicio.objects.filter(id=servicio_id).first()
    if servicio:
        data = {
            'nombre': servicio.nombre_servicio,
            'descripcion': servicio.descripcion,
            'precio': servicio.precio_sugerido,
            # Asegúrate de manejar relaciones nulas
            'metodo': servicio.metodo.metodo if servicio.metodo else 'No disponible',
            # Agrega otros campos que necesites
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Servicio no encontrado'}, status=404)

# AGREGAR NUEVA COTIZACION
def cotizacion_form(request,persona_id, cotizacion_id=None):
    persona = get_object_or_404(Persona, id=persona_id)
    
    if cotizacion_id:
        cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id, persona=persona)
    else:
        cotizacion = None
    servicios = list(Servicio.objects.all().values('id', 'nombre_servicio'))  # Asegúrate de ajustar los campos según tu modelo
    servicios_json = json.dumps(servicios)  # Convertir la lista de diccionarios a JSON
    if request.method == 'POST':
        
        if cotizacion:
            cotizacion_form=CotizacionForm(request.POST, instance=cotizacion)
            concepto_formset=ConceptoFormSet(request.POST, instance=cotizacion)
        else:
            cotizacion_form = CotizacionForm(request.POST)
            concepto_formset = ConceptoFormSet(request.POST)
            if cotizacion_form.is_valid() and concepto_formset.is_valid():
                try:
                    with transaction.atomic():  # Usar una transacción atómica para asegurar la atomicidad
                        cotizacion = cotizacion_form.save(commit=False)
                        cotizacion.persona = persona
                            
                        cotizacion.id_personalizado = generate_new_id_personalizado()
                        cotizacion.save()

                        conceptos = concepto_formset.save(commit=False)
                        for concepto in conceptos:
                            concepto.cotizacion = cotizacion
                            concepto.save()

                        cotizacion.subtotal = sum(
                        c.cantidad_servicios * c.precio for c in cotizacion.conceptos.all())
                        cotizacion.iva = cotizacion.subtotal * Decimal(cotizacion.tasa_iva)
                        cotizacion.total = cotizacion.subtotal + cotizacion.iva
                        cotizacion.save()
                        # Generar PDF y guardar en el modelo
                        pdf_data = generar_pdf_cotizacion(request, cotizacion)
                        cotizacion.cotizacion_pdf.save(f"cotizacion_{cotizacion.id_personalizado}.pdf", ContentFile(pdf_data))
                        cotizacion.save()
                        # Verificar si la persona ya existe en la tabla de prospectos
                        if not Prospecto.objects.filter(persona=persona).exists():
                            prospecto = Prospecto(persona=persona)
                            prospecto.save()
                        messages.success(request, 'Cotización creada con éxito.')
                        return redirect('cotizacion_detalle', pk=cotizacion.id)
                except IntegrityError:
                    messages.error(
                        request, 'Hubo un error al crear la cotización. Inténtalo de nuevo.')
            else:
                print(cotizacion_form.errors)
                print(concepto_formset.errors)
                messages.error(
                    request, 'Hubo un error en el formulario. Por favor, revisa los campos e intenta nuevamente.')
    else:
        if cotizacion:
            cotizacion_form = CotizacionForm(instance=cotizacion)
            concepto_formset = ConceptoFormSet(instance=cotizacion)
        else:
            cotizacion_form = CotizacionForm()
            concepto_formset = ConceptoFormSet()
    return render(request, 'accounts/cotizaciones/cotizaciones_registro.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
        'cliente': persona,
        'servicios_json': servicios_json,
        'servicio_form':ServicioForm(),
        'metodos': Metodo.objects.all(),
        'metodo_form': MetodoForm(),
    })

# INTERFAZ DE DETALLES DE CADA COTIZACION
def cotizacion_detalle(request, pk):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    conceptos = cotizacion.conceptos.all()
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio
    
    tasa_iva = cotizacion.tasa_iva * 100
    # Obtener las órdenes de trabajo relacionadas con la cotización
    ordenes_trabajo = OrdenTrabajo.objects.filter(cotizacion=cotizacion) 
    
    return render(request, 'accounts/cotizaciones/cotizacion_detalle.html', {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'cotizacion': cotizacion,
        'conceptos': conceptos,
        'tasa_iva': tasa_iva,
        'ordenes_trabajo': ordenes_trabajo,
    })

# INTERFAZ PARA ELIMINAR COTIZACION
def cotizacion_delete(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    if request.method == "POST":
        cotizacion.delete()
        # Redirigir a la lista de cotizaciones después de la eliminación
        return redirect('cotizaciones_list')
    return render(request, 'accounts/cotizaciones/eliminar_colitazion.html', {'cotizacion': cotizacion})

# Vista para editar cotización
def cotizacion_edit(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    ConceptoFormSet = inlineformset_factory(Cotizacion, Concepto, form=ConceptoForm, extra=1, can_delete=True)
    servicios = list(Servicio.objects.all().values('id', 'nombre_servicio'))  # Asegúrate de ajustar los campos según tu modelo
    servicios_json = json.dumps(servicios)  # Convertir la lista de diccionarios a JSON

    if request.method == 'POST':
        cotizacion_form = CotizacionChangeForm(request.POST, instance=cotizacion)
        concepto_formset = ConceptoFormSet(request.POST, instance=cotizacion)

        if cotizacion_form.is_valid() and concepto_formset.is_valid():
            try:
                with transaction.atomic():
                    cotizacion = cotizacion_form.save(commit=False)
                    cotizacion.save()

                    concepto_formset.save()

                    # Recalcular subtotal, iva y total de todos los conceptos relacionados con esta cotización
                    conceptos = cotizacion.conceptos.all()
                    subtotal = sum([concepto.cantidad_servicios * concepto.precio for concepto in conceptos])
                    tasa_iva_decimal = Decimal(cotizacion.tasa_iva)
                    iva = subtotal * tasa_iva_decimal
                    total = subtotal + iva

                    # Actualizar los valores en la instancia de cotización
                    cotizacion.subtotal = subtotal
                    cotizacion.iva = iva
                    cotizacion.total = total
                    cotizacion.save()

                    messages.info(request, 'Cotización editada exitosamente.')
                    return redirect('cotizacion_detalle', pk=cotizacion.id)
            except IntegrityError:
                messages.error(request, 'Hubo un error al editar la cotización. Inténtalo de nuevo.')
        else:
            messages.error(request, 'Hubo un error en el formulario. Por favor, revisa los campos e intenta nuevamente.')
    else:
        cotizacion_form = CotizacionChangeForm(instance=cotizacion)
        concepto_formset = ConceptoFormSet(instance=cotizacion)

    context = {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
        'cotizacion': cotizacion,
        'cliente': cotizacion.persona,
        'servicios_json': servicios_json,
        'servicio_form': ServicioForm(),
        'metodos': Metodo.objects.all(),
        'metodo_form': MetodoForm(),
        'edit': True  # Esta bandera se puede usar para ajustar la interfaz según si es edición o creación
    }
    return render(request, 'accounts/cotizaciones/cotizaciones_editar.html', context)

# Vista para duplicar una cotización
def cotizacion_duplicar(request, pk):
    cotizacion_original = get_object_or_404(Cotizacion, id=pk)
    
    # Crear una nueva instancia de Cotizacion con los mismos datos que la original
    cotizacion_nueva = Cotizacion.objects.create(
        persona=cotizacion_original.persona,
        fecha_solicitud=cotizacion_original.fecha_solicitud,
        fecha_caducidad=cotizacion_original.fecha_caducidad,
        metodo_pago=cotizacion_original.metodo_pago,
        tasa_iva=cotizacion_original.tasa_iva,
        notas=cotizacion_original.notas,
        correos_adicionales=cotizacion_original.correos_adicionales,
        subtotal=cotizacion_original.subtotal,
        iva=cotizacion_original.iva,
        total=cotizacion_original.total,
        estado=False  # Estado inicial como "No Aceptado"
    )
    cotizacion_nueva.id_personalizado = cotizacion_nueva.generate_new_id_personalizado()
    cotizacion_nueva.save()

    # Duplicar los conceptos asociados
    conceptos_originales = Concepto.objects.filter(cotizacion=cotizacion_original)
    for concepto in conceptos_originales:
        Concepto.objects.create(
            cotizacion=cotizacion_nueva,
            servicio=concepto.servicio,
            cantidad_servicios=concepto.cantidad_servicios,
            precio=concepto.precio,
            notas=concepto.notas
        )

    messages.success(request, 'Cotización duplicada con éxito.')
    return redirect('cotizacion_detalle', pk=cotizacion_nueva.id)

# VISTA PARA VER ARCHIVO PDF COTIZACION
def cotizacion_pdf(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    # Verificar si el archivo PDF existe
    if cotizacion.cotizacion_pdf:
        # Retornar el archivo PDF guardado
        return FileResponse(cotizacion.cotizacion_pdf.open(), content_type='application/pdf')
    else:
        raise Http404("El archivo PDF no se encuentra.")

# VISTA PARA VER ARCHIVO PDF ORDEN PEDIDO
def ver_orden_pedido(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    if not cotizacion.orden_pedido_pdf:
        raise Http404("El archivo PDF de la orden de pedido no se encuentra.")
    return FileResponse(cotizacion.orden_pedido_pdf.open(), content_type='application/pdf')

# VISTA PARA GENERAR PDF Y GUARDARLO EN BD
def generar_pdf_cotizacion(request,cotizacion):
    conceptos = cotizacion.conceptos.all()
    org = get_unica_organizacion()
    formato = org.f_cotizacion
    user = request.user if request.user.is_authenticated else None
    
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio
    
    current_date = datetime.now().strftime("%Y/%m/%d")
    logo_url = request.build_absolute_uri('/static/img/logo.png')  # Necesitas obtener este request de alguna manera, o ajustar para no usar request aquí
    marca = request.build_absolute_uri('/static/img/Imagen 21.jpg')

    context = {
        'org': org,
        'org_form': formato,
        'user': user,
        'cotizacion': cotizacion,
        'conceptos': conceptos,
        'current_date': current_date,
        'logo_url': logo_url,
        'marca':marca,
    }

    html_string = render_to_string(
        'accounts/cotizaciones/cotizacion_platilla.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())  # Ajustar según sea necesario sin request
    pdf = html.write_pdf()

    # Devolver los datos binarios del PDF
    return pdf

# VISTA PARA CAMBIAR ESTADO DE COTIZACIÓN
def actualizar_estado(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    cotizacion.estado = True
    # aqui quiero borrar el prospecto que sea igual a cotizacion.persona
        # Intenta obtener y borrar el prospecto que coincide con la persona de la cotización
    prospecto = Prospecto.objects.filter(persona=cotizacion.persona).first()
    if prospecto:
        prospecto.delete()
        messages.success(request, 'El estado de la cotización ha sido actualizado a Aceptado y el prospecto ha sido eliminado.')
    else:
        messages.success(request, 'El estado de la cotización ha sido actualizado a Aceptado.')
    
    cotizacion.save()
    return redirect('cotizacion_detalle', pk=cotizacion.id)