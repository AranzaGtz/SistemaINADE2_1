from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import Cotizacion, Concepto
from accounts.forms import CotizacionForm, ConceptoFormSet
from django.contrib import messages

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