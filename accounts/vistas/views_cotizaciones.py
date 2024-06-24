from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import Cotizacion, Concepto
from accounts.forms import CotizacionForm, ConceptoFormSet

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
            cotizacion.subtotal = sum([c.cantidad_servicios * c.precio for c in conceptos])
            cotizacion.iva = cotizacion.subtotal * (cotizacion.tasa_iva / 100)
            cotizacion.total = cotizacion.subtotal + cotizacion.iva
            cotizacion.save()
            return redirect('cotizacion_detalle', pk=cotizacion.pk)
    else:
        cotizacion_form = CotizacionForm()
        concepto_formset = ConceptoFormSet()

    return render(request, 'accounts/cotizaciones/cotizaciones_registro.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
    })

def cotizacion_detalle(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    conceptos = cotizacion.conceptos.all()
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio
    
    return render(request, 'accounts/cotizaciones/cotizacion_detalle.html', {
        'cotizacion': cotizacion,
        'conceptos': conceptos,
    })

def crear_cotizacion(request):
    if request.method == 'POST':
        cotizacion_form = CotizacionForm(request.POST)
        concepto_formset = ConceptoFormSet(request.POST)
        
        if cotizacion_form.is_valid() and concepto_formset.is_valid():
            cotizacion = cotizacion_form.save()
            conceptos = concepto_formset.save(commit=False)
            for concepto in conceptos:
                concepto.cotizacion = cotizacion
                concepto.save()
            cotizacion.subtotal = sum([c.cantidad_servicios * c.precio for c in conceptos])
            cotizacion.iva = cotizacion.subtotal * (cotizacion.tasa_iva / 100)
            cotizacion.total = cotizacion.subtotal + cotizacion.iva
            cotizacion.save()
            return redirect('cotizacion_detalle', pk=cotizacion.pk)
    else:
        cotizacion_form = CotizacionForm()
        concepto_formset = ConceptoFormSet()
    
    return render(request, 'accounts/cotizaciones/cotizaciones.html', {
        'cotizacion_form': cotizacion_form,
        'concepto_formset': concepto_formset,
    })

