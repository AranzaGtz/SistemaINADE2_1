from datetime import datetime
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import Cotizacion, Concepto, Organizacion, Formato, CustomUser
from accounts.forms import ConceptoForm, CotizacionForm, CotizacionChangeForm, ConceptoFormSet, ConceptoChangeFormSet, TerminosForm
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from weasyprint import HTML # type: ignore #AQUI SALE WARNING: No se ha podido resolver la importación "weasyprint".
from django.template.loader import render_to_string  # Asegúrate de importar render_to_string
import tempfile
import uuid
from django.db import IntegrityError, transaction

# VISTA DE COTIZACIONES
def cotizaciones_list(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, "accounts/cotizaciones/cotizaciones.html",{'cotizaciones': cotizaciones})

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
                    
                    cotizacion.subtotal = sum([c.cantidad_servicios * c.precio for c in cotizacion.conceptos.all()])
                    cotizacion.iva = cotizacion.subtotal * (cotizacion.tasa_iva / 100)
                    cotizacion.total = cotizacion.subtotal + cotizacion.iva
                    cotizacion.save()
                    
                    messages.success(request, 'Cotización creada con éxito.')
                    return redirect('cotizacion_detalle', pk=cotizacion.id)
            except IntegrityError:
                messages.error(request, 'Hubo un error al crear la cotización. Inténtalo de nuevo.')
        else:
            print(cotizacion_form.errors)
            print(concepto_formset.errors)
            messages.error(request, 'Hubo un error en el formulario. Por favor, revisa los campos e intenta nuevamente.')
    else:
        cotizacion_form = CotizacionForm()
        concepto_formset = ConceptoFormSet()
    
    return render(request, 'accounts/cotizaciones/cotizaciones_registro.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
    })

# INTERFAZ DE DETALLES DE CADA COTIZACION
def cotizacion_detalle(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    conceptos = cotizacion.conceptos.all()
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio

    cotizacion_persona=cotizacion.persona.id
    return render(request, 'accounts/cotizaciones/cotizacion_detalle.html', {
        'cotizacion': cotizacion,
        'conceptos': conceptos,
    })

# INTERFAZ PARA ELIMINAR COTIZACION
def cotizacion_delete(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    if request.method == "POST":
        cotizacion.delete()
        return redirect('cotizaciones_list')  # Redirigir a la lista de cotizaciones después de la eliminación
    return render(request, 'accounts/cotizaciones/eliminar_colitazion.html', {'cotizacion': cotizacion})

# VISTA PARA EDITAR COTIZACION
def cotizacion_edit(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk) # Obtiene una instancia del modelo de cotizacion desde pk, si no encuentra devuelve error 404
    # print(f"Fecha Solicitada: {cotizacion.fecha_solicitud}, Fecha Caducidad: {cotizacion.fecha_caducidad}")
    if request.method == 'POST': # Si el formulario a sido enviado
        # Crear instancias de los formularios CotizacionChangeForm y ConceptoChangeFormSet, pre-poblados con los datos enviados en la solicitud POST.
        cotizacion_form = CotizacionChangeForm(request.POST, instance=cotizacion)
        concepto_formset = ConceptoChangeFormSet(request.POST, instance=cotizacion)
        # request.post contiene los datos enviados, instance = cotizacion vincula los formularios a la existente de cotizacion

        if cotizacion_form.is_valid() and concepto_formset.is_valid(): # verifica que los formularios sean validos
            # 
            cotizacion = cotizacion_form.save()
            conceptos = concepto_formset.save(commit=False)
            for concepto in conceptos:
                concepto.cotizacion = cotizacion
                concepto.save()
            for concepto in concepto_formset.deleted_objects:
                concepto.delete()
            
            cotizacion.subtotal = sum([c.cantidad_servicios * c.precio for c in conceptos])
            cotizacion.iva = cotizacion.subtotal * (cotizacion.tasa_iva / 100)
            cotizacion.total = cotizacion.subtotal + cotizacion.iva
            cotizacion.save()
            messages.info(request,'Editando cotización.')
            # Redirigir al usuario a la vista de detalles de la cotización después de guardar los cambios.
            return redirect('cotizacion_detalle', pk=cotizacion.id)
    else:
        # Inicializar los formularios con los datos actuales de la cotización y sus conceptos cuando la solicitud no es POST (es decir, en GET).
        cotizacion_form = CotizacionChangeForm(instance=cotizacion)
        concepto_formset = ConceptoChangeFormSet(instance=cotizacion)
    # cotizaciones_editar.html con los formularios de cotización y conceptos.
    return render(request, 'accounts/cotizaciones/cotizaciones_editar.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
        'cotizacion': cotizacion,
        'edit': True
    })
   
# VISTA PARA DUPLICAR COTIZACION
def cotizacion_duplicar(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    conceptos = cotizacion.conceptos.all()

    if request.method == 'POST':
        cotizacion_form = CotizacionForm(request.POST)
        concepto_formset = modelformset_factory(Concepto, form=ConceptoForm, extra=0)
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
        concepto_formset = modelformset_factory(Concepto, form=ConceptoForm, extra=0)
        formset = concepto_formset(queryset=conceptos)

    return render(request, 'accounts/cotizaciones/cotizacion_duplicar.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': formset
    })

def generate_new_id_personalizado():
    last_cotizacion = Cotizacion.objects.order_by('id_personalizado').last()
    if not last_cotizacion:
        return '0001'
    last_id = last_cotizacion.id_personalizado
    new_id = int(last_id) + 1
    return str(new_id).zfill(4)

# VISTA PARA GENERAR ARCHIVO PDF
def cotizacion_pdf(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    conceptos = cotizacion.conceptos.all()
    ogr = get_object_or_404(Organizacion,id=1)
    formato = get_object_or_404(Formato, id=1)
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        username = request.user.username
        user = get_object_or_404(CustomUser, username=username)
    # Ahora puedes trabajar con el objeto 'user'

    
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio
    # Construir la URL absoluta del archivo de la imagen
    logo_url = request.build_absolute_uri('/static/img/logo.png')
    current_date = datetime.now().strftime("%Y/%m/%d")
    context = {
        'org':ogr,
        'org_form':formato,
        'user': user,
        'cotizacion': cotizacion,
        'conceptos': conceptos,
        'current_date': current_date,
        'logo_url': logo_url,  # Agregar la URL de la imagen al contexto
    }

    html_string = render_to_string('accounts/cotizaciones/cotizacion_platilla.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())  # Asegurarse de que las URLs sean absolutas
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="cotizacion_{cotizacion.id_personalizado}.pdf"'
    return response

# VISTA PARA MODIFICAR NUESTRA INFORMACION DE FORMATO
def terminos_avisos(request):
    formato = get_object_or_404(Formato, pk=1)
    if request.method == 'POST':
        form = TerminosForm(request.POST, instance=formato)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la vista deseada después de guardar
    else:
        form = TerminosForm(instance=formato)
    return render(request, 'accounts/cotizaciones/terminos.html', {'form': form})
