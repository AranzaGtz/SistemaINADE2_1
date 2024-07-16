from datetime import datetime
from urllib import request
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from accounts.helpers import get_formato_default, get_unica_organizacion
from accounts.models import Cotizacion, Concepto, Empresa, InformacionContacto, Organizacion, Formato, CustomUser, Persona, Prospecto, Servicio, Titulo
from accounts.forms import ConceptoForm, CotizacionForm, CotizacionChangeForm, ConceptoFormSet, DireccionForm, EmpresaForm, PersonaForm, ProspectoForm, TerminosForm
from django.contrib import messages
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from weasyprint import HTML  # type: ignore
from django.template.loader import render_to_string
from django.db import IntegrityError, transaction
from django.core.files.base import ContentFile
from io import BytesIO

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
    # Inicializar la consulta de cotizaciones
    cotizaciones = Cotizacion.objects.all()
    cotizacion_form = CotizacionForm()
    concepto_formset = ConceptoFormSet()

    # Inicializar formularios para crear prospectos
    titulos = Titulo.objects.all()
    empresas = Empresa.objects.all()
    persona_form = PersonaForm()
    empresa_form = EmpresaForm()
    prospecto_from = ProspectoForm()

    context = {
        'cotizaciones': cotizaciones,
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
        'titulos': titulos,
        'empresas': empresas,
        'persona_form': persona_form,
        'empresa_form': empresa_form,
        'prospecto_form': prospecto_from
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
def cotizacion_form(request):
    if request.method == 'POST':
        cotizacion_form = CotizacionForm(request.POST)
        concepto_formset = ConceptoFormSet(request.POST)
        

        if cotizacion_form.is_valid() and concepto_formset.is_valid():
            try:
                with transaction.atomic():  # Usar una transacción atómica para asegurar la atomicidad
                    cotizacion = cotizacion_form.save(commit=False)
                    cotizacion.id_personalizado = generate_new_id_personalizado()
                    cotizacion.save()

                    conceptos = concepto_formset.save(commit=False)
                    for concepto in conceptos:
                        concepto.cotizacion = cotizacion
                        concepto.save()

                    cotizacion.subtotal = sum(
                        [c.cantidad_servicios * c.precio for c in cotizacion.conceptos.all()])
                    cotizacion.iva = cotizacion.subtotal * \
                        (cotizacion.tasa_iva / 100)
                    cotizacion.total = cotizacion.subtotal + cotizacion.iva
                    cotizacion.save()
                    # Generar PDF y guardar en el modelo
                    pdf_data = generar_pdf_cotizacion(request, cotizacion)
                    cotizacion.cotizacion_pdf.save(f"cotizacion_{cotizacion.id_personalizado}.pdf", ContentFile(pdf_data))
                    cotizacion.save()
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
        cotizacion_form = CotizacionForm()
        concepto_formset = ConceptoFormSet()
        
        # Inicializar formularios para crear prospectos
        titulos = Titulo.objects.all()
        empresas = Empresa.objects.all()
        persona_form = PersonaForm()
        empresa_form = EmpresaForm()
        prospecto_from = ProspectoForm()
        
        context={
            'cotizaxion_form': cotizacion_form,
            'concepto_formset': concepto_formset,
            'titulos': titulos,
            'empresas': empresas,
            'persona_form': persona_form,
            'empresa_form': empresa_form,
            'prospecto_form': prospecto_from
        }

    return render(request, 'accounts/cotizaciones/cotizaciones_registro.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
    })

# VISTA PARA CREAR CLIENTES DESDE MODAL
def cotizaciones_prospecto_create(request):
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        empresa_form = EmpresaForm(
            request.POST) if 'crear_empresa_checkbox' in request.POST else None
        direccion_form = DireccionForm(
            request.POST) if 'crear_empresa_checkbox' in request.POST else None

        if persona_form.is_valid():
            # Guardar la información de contacto primero
            informacion_contacto = InformacionContacto(
                correo_electronico=persona_form.cleaned_data['correo_electronico'],
                telefono=persona_form.cleaned_data['telefono'],
                celular=persona_form.cleaned_data['celular'],
                fax=persona_form.cleaned_data['fax']
            )
            informacion_contacto.save()

            # Comprobar si se seleccionó una empresa existente o se necesita crear una nueva
            if 'crear_empresa_checkbox' in request.POST:
                if empresa_form and empresa_form.is_valid() and direccion_form and direccion_form.is_valid():
                    direccion = direccion_form.save()
                    empresa = empresa_form.save(commit=False)
                    empresa.direccion = direccion
                    empresa.save()
                else:
                    messages.error(
                        request, 'Por favor, corrige los errores en el formulario de empresa.')
                    return render(request, 'accounts/cotizaciones/cotizaciones_preregistro.html', {
                        'persona_form': persona_form,
                        'empresa_form': empresa_form,
                        'direccion_form': direccion_form,
                        'empresas': Empresa.objects.all(),
                        'titulos': Titulo.objects.all()
                    })
            elif 'empresa' in request.POST and request.POST['empresa']:
                empresa = Empresa.objects.get(id=request.POST['empresa'])
            else:
                messages.error(
                    request, 'Por favor, selecciona o crea una empresa.')
                return render(request, 'accounts/cotizaciones/cotizaciones_preregistro.html', {
                    'persona_form': persona_form,
                    'empresa_form': empresa_form,
                    'empresas': Empresa.objects.all(),
                    'titulos': Titulo.objects.all()
                })

            # Crear el cliente
            persona = persona_form.save(commit=False)
            persona.empresa = empresa
            persona.informacion_contacto = informacion_contacto
            persona.save()

            # Crear el prospecto
            prospecto = Prospecto(persona=persona)
            prospecto.save()

            messages.success(request, 'Prospecto creado.')
            
            cotizacion_form = CotizacionForm(initial={'persona': persona, 'metodo_pago': prospecto.persona.empresa.moneda})
            
            
            concepto_formset = ConceptoFormSet()
            return render(request, 'accounts/cotizaciones/cotizaciones_registro.html', {
                'cotizacion_form': cotizacion_form,
                'concepto_formset': concepto_formset,
                'empresa':empresa.nombre_empresa,
                'persona':persona,
                'metodo_pago': empresa.moneda,
                'informacionContacto': informacion_contacto,
                'rfc': empresa.rfc
            })

        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        persona_form = PersonaForm()
        empresa_form = EmpresaForm()
        direccion_form = DireccionForm()

    titulos = Titulo.objects.all()
    context = {
        'persona_form': persona_form,
        'empresa_form': empresa_form,
        'direccion_form': direccion_form,
        'empresas': Empresa.objects.all(),
        'titulos': titulos,
    }
    return render(request, 'accounts/cotizaciones/cotizaciones_preregistro.html', context)

# INTERFAZ DE DETALLES DE CADA COTIZACION
def cotizacion_detalle(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    conceptos = cotizacion.conceptos.all()
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio

    cotizacion_persona = cotizacion.persona.id
    return render(request, 'accounts/cotizaciones/cotizacion_detalle.html', {
        'cotizacion': cotizacion,
        'conceptos': conceptos,
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

    if request.method == 'POST':
        cotizacion_form = CotizacionChangeForm(request.POST, instance=cotizacion)
        concepto_formset = ConceptoFormSet(request.POST, instance=cotizacion)

        if cotizacion_form.is_valid() and concepto_formset.is_valid():
            # Guardar la instancia de cotización y los conceptos asociados
            cotizacion = cotizacion_form.save()
            concepto_formset.save()

            # Recalcular subtotal, iva y total de todos los conceptos relacionados con esta cotización
            with transaction.atomic():
                conceptos = cotizacion.conceptos.all()
                subtotal = sum([concepto.cantidad_servicios * concepto.precio for concepto in conceptos])
                iva = subtotal * (cotizacion.tasa_iva / 100)
                total = subtotal + iva

                # Actualizar los valores en la instancia de cotización
                cotizacion.subtotal = subtotal
                cotizacion.iva = iva
                cotizacion.total = total
                cotizacion.save()

            messages.info(request, 'Cotización editada exitosamente.')
            return redirect('cotizacion_detalle', pk=cotizacion.id)
    else:
        cotizacion_form = CotizacionChangeForm(instance=cotizacion)
        concepto_formset = ConceptoFormSet(instance=cotizacion)
        
    context = {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
        'cotizacion': cotizacion,
        'persona': cotizacion.persona.nombre,
        'empresa': cotizacion.persona.empresa.nombre_empresa,
        'rfc': cotizacion.persona.empresa.rfc,
        'informacionContacto': cotizacion.persona.informacion_contacto,
        'edit': True  # Esta bandera se puede usar para ajustar la interfaz según si es edición o creación
    }
    return render(request, 'accounts/cotizaciones/cotizaciones_editar.html', context)

# VISTA PARA DUPLICAR COTIZACION
def cotizacion_duplicar(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    conceptos = cotizacion.conceptos.all()

    if request.method == 'POST':
        cotizacion_form = CotizacionForm(request.POST)
        concepto_formset = modelformset_factory(
            Concepto, form=ConceptoForm, extra=0)
        formset = concepto_formset(request.POST, queryset=conceptos)

        if cotizacion_form.is_valid() and formset.is_valid():
            nueva_cotizacion = cotizacion_form.save(commit=False)
            nueva_cotizacion.id = None  # Esto asegurará que se cree una nueva instancia

            # Generar un nuevo id_personalizado único
            nueva_cotizacion.id_personalizado = generate_new_id_personalizado()

            nueva_cotizacion.save()

            for form in formset:
                nuevo_concepto = form.save(commit=False)
                nuevo_concepto.id = None  # Crear una nueva instancia del concepto
                nuevo_concepto.cotizacion = nueva_cotizacion
                nuevo_concepto.save()

            # Calcular y actualizar los valores de subtotal, IVA y total
            nueva_cotizacion.subtotal = nueva_cotizacion.calculate_subtotal()
            nueva_cotizacion.iva = nueva_cotizacion.calculate_iva()
            nueva_cotizacion.total = nueva_cotizacion.calculate_total()
            nueva_cotizacion.save()

            return redirect('cotizacion_detalle', pk=nueva_cotizacion.id)
    else:
        cotizacion_form = CotizacionForm(instance=cotizacion)
        concepto_formset = modelformset_factory(
            Concepto, form=ConceptoForm, extra=0)
        formset = concepto_formset(queryset=conceptos)

    return render(request, 'accounts/cotizaciones/cotizacion_duplicar.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': formset
    })

# VISTA PARA GENERAR ARCHIVO PDF
def cotizacion_pdf(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    # Verificar si el archivo PDF existe
    if cotizacion.cotizacion_pdf:
        # Retornar el archivo PDF guardado
        return FileResponse(cotizacion.cotizacion_pdf.open(), content_type='application/pdf')
    else:
        raise Http404("El archivo PDF no se encuentra.")

# VISTA PARA GENERAR PDF Y GUARDARLO EN BD
def generar_pdf_cotizacion(request,cotizacion):
    conceptos = cotizacion.conceptos.all()
    org = get_unica_organizacion()
    formato = get_formato_default()
    user = request.user if request.user.is_authenticated else None
    
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio
    
    current_date = datetime.now().strftime("%Y/%m/%d")
    logo_url = request.build_absolute_uri('/static/img/logo.png')  # Necesitas obtener este request de alguna manera, o ajustar para no usar request aquí

    context = {
        'org': org,
        'org_form': formato,
        'user': user,
        'cotizacion': cotizacion,
        'conceptos': conceptos,
        'current_date': current_date,
        'logo_url': logo_url,
    }

    html_string = render_to_string(
        'accounts/cotizaciones/cotizacion_platilla.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())  # Ajustar según sea necesario sin request
    pdf = html.write_pdf()

    # Devolver los datos binarios del PDF
    return pdf

