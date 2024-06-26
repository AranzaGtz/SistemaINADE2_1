from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import Cotizacion, Concepto
from accounts.forms import CotizacionForm, ConceptoFormSet
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from weasyprint import HTML #AQUI SALE WARNING: No se ha podido resolver la importación "weasyprint".
from django.template.loader import render_to_string  # Asegúrate de importar render_to_string
import tempfile

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
            cotizacion = cotizacion_form.save()
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
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    print(f"Fecha Solicitada: {cotizacion.fecha_solicitud}, Fecha Caducidad: {cotizacion.fecha_caducidad}")
    if request.method == 'POST':
        cotizacion_form = CotizacionForm(request.POST, instance=cotizacion)
        concepto_formset = ConceptoFormSet(request.POST, instance=cotizacion)
        
        if cotizacion_form.is_valid() and concepto_formset.is_valid():
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
            return redirect('cotizacion_detalle', pk=cotizacion.id)
    else:
        cotizacion_form = CotizacionForm(instance=cotizacion)
        concepto_formset = ConceptoFormSet(instance=cotizacion)

    return render(request, 'accounts/cotizaciones/cotizaciones_registro.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
        'cotizacion': cotizacion,
        'edit': True
    })
    
# VISTA PARA GENERAR ARCHIVO PDF
def cotizacion_pdf(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    conceptos = cotizacion.conceptos.all()
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio
    # Construir la URL absoluta del archivo de la imagen
    logo_url = request.build_absolute_uri('/static/img/logo.png')

    context = {
        'cotizacion': cotizacion,
        'conceptos': conceptos,
        'logo_url': logo_url,  # Agregar la URL de la imagen al contexto
    }

    html_string = render_to_string('accounts/cotizaciones/cotizacion_platilla.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())  # Asegurarse de que las URLs sean absolutas
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="cotizacion_{cotizacion.id_personalizado}.pdf"'
    return response