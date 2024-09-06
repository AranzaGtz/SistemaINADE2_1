from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from accounts.forms import AlmacenForm, SucursalForm
from accounts.models import Cotizacion, OrdenTrabajo, OrdenTrabajoConcepto, Organizacion, Servicio
from facturacion.models import ConceptoFactura, Factura
from .forms import CSDForm, ConceptoFacturaFormSet, FacturaEncabezadoForm, FacturaPieForm, FacturaTotalesForm, ServicioFormset
from django.contrib import messages
import base64

def agregar_sucursal(request):
    org = Organizacion.objects.first()  # Obtén la primera organización
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            sucursal = form.save(commit=False)
            sucursal.organizacion = org  # Asigna la organización
            sucursal.save()  # Guarda la sucursal

            # Retorna el script para actualizar el select en la ventana principal y cierra la ventana
            return HttpResponse(f"""
                <script>
                    window.opener.actualizarSelectSucursal({{
                        nombre: "{sucursal.nombre}", 
                        sucursal: "{sucursal.direccion}",
                        organizacion: "{org.id}"
                    }});
                    window.close();
                </script>
            """)
    else:
        form = SucursalForm()

    return render(request, 'facturacion/agregar_sucursal.html', {'form': form})

def agregar_almacen (request):
    org = Organizacion.objects.first()  # Obtén la primera organización
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        if form.is_valid():
            almacen = form.save(commit=False)
            almacen.organizacion = org  # Asigna la organización
            almacen.save()  # Guarda la almacen

            # Retorna el script para actualizar el select en la ventana principal y cierra la ventana
            return HttpResponse(f"""
                <script>
                    window.opener.actualizarSelectAlmacen({{
                        nombre: "{almacen.nombre}", 
                        almacen: "{almacen.direccion}",
                        organizacion: "{org.id}"
                    }});
                    window.close();
                </script>
            """)
    else:
        form = AlmacenForm()

    return render(request, 'facturacion/agregar_almacen.html', {'form': form})

def obtener_datos_cotizacion(request, cotizacion_id):
    try:
        cotizacion = Cotizacion.objects.get(id=cotizacion_id)
        conceptos = cotizacion.conceptos.all()
        conceptos_data = [{
            'servicio': concepto.servicio.nombre_servicio,
            'cantidad_servicios': concepto.cantidad_servicios,
            'precio': concepto.precio,
            'total': concepto.cantidad_servicios * concepto.precio
        } for concepto in conceptos]

        data = {
            'subtotal': cotizacion.subtotal,
            'iva': cotizacion.iva,
            'total': cotizacion.total,
            'metodo_pago': cotizacion.metodo_pago,
            'tasa_iva': cotizacion.tasa_iva,
            'notas': cotizacion.notas,
            'conceptos': conceptos_data
        }

        return JsonResponse(data)
    except Cotizacion.DoesNotExist:
        return JsonResponse({'error': 'Cotización no encontrada'}, status=404)

def crear_factura(request, id_personalizado):
    orden = get_object_or_404(OrdenTrabajo, id_personalizado=id_personalizado)
    conceptos = OrdenTrabajoConcepto.objects.filter(orden_de_trabajo=id_personalizado)
    servicios = Servicio.objects.all()
    
    # Creamos la lista de datos iniciales para el formset de conceptos
    initial_conceptos = [{
        'servicio': concepto.concepto.servicio,
        'cantidad_servicios': concepto.concepto.cantidad_servicios,
        'precio': concepto.concepto.precio,
        'importe': concepto.concepto.importe,
    } for concepto in conceptos]
    
    concepto_formset = ConceptoFacturaFormSet(initial=initial_conceptos)

    # En este caso inicializamos los formularios vacios
    encabezado_form = FacturaEncabezadoForm(initial={'orden': orden.id_personalizado,'tipo_moneda': orden.cotizacion.metodo_pago})
    form = FacturaEncabezadoForm()
    pie_form = FacturaPieForm(initial={'direccion': orden.direccion,'comentarios': orden.cotizacion.notas,'correos': orden.cotizacion.correos_adicionales})
    totales_form = FacturaTotalesForm()
    concepto_formset= ConceptoFacturaFormSet(initial=initial_conceptos)
    servicio_formset = ServicioFormset()
    
    if request.method == 'POST':
        # Inicializamos los formularios con POST
        encabezado_form = FacturaEncabezadoForm(request.POST)
        form = FacturaEncabezadoForm(request.POST,initial={'orden': orden.id_personalizado})
        pie_form = FacturaPieForm(request.POST, initial={'direccion': orden.direccion})
        totales_form = FacturaTotalesForm(request.POST)
        concepto_formset = ConceptoFacturaFormSet(request.POST)
        servicio_formset = ServicioFormset(request.POST)
        
        # Validamos todos los formularios
        if encabezado_form.is_valid() and form.is_valid() and pie_form.is_valid() and totales_form.is_valid() and concepto_formset.is_valid() and servicio_formset.is_valid():
            # Guardar encabezado, cuerpo y pie que comparten la misma instancia
            factura = encabezado_form.save(commit=False)  # No guardamos en la BD todavía
            factura = form.save(commit=False)
            factura = pie_form.save(commit=False)
            factura = totales_form.save(commit=False)
            factura.save() # Guardamos en la BD
            
            # Guardar los formsets (Conceptos y Servicios)
            concepto_formset.instance = factura
            concepto_formset.save()
            servicio_formset.instance = factura
            
            # Redirigir a la página de detalle de la factura u otra vista
            return redirect('crear_factura', pk=factura.pk)
    context = {
        'orden': orden,
        'encabezado_form': encabezado_form,
        'form': form,
        'pie_form':pie_form,
        'totales_form': totales_form,
        'concepto_formset': concepto_formset,
        'servicio_formset': servicio_formset,
        'totales_form':totales_form,
        'conceptos': conceptos,
        'servicios':servicios
    }
    return render(request, 'facturacion/formulario.html', context)

@login_required
def cargar_csd(request):
    # https://apisandbox.facturama.mx/guias/api-multi/csds
    if request.method == 'POST':
        form = CSDForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar en la BD
            csd = form.save(commit=False)
            rfc = form.cleaned_data['rfc']
            cer_file = form.cleaned_data['cer_file']
            key_file = form.cleaned_data['key_file']
            key_password = form.cleaned_data['password']

            cer_base64 = convertir_a_base64(cer_file)
            key_base64 = convertir_a_base64(key_file)

            csd_data = {
                "Rfc": rfc,
                "Certificate": cer_base64,
                "PrivateKey": key_base64,
                "PrivateKeyPassword": key_password,
            }

            print(csd_data)

            # URL de la API de Facturama
            url = "https://apisandbox.facturama.mx/api-lite/csds"
            username = "examples@inade.mx" # nombre de usuario
            password = "Puebla4990"
            response = requests.post(
                url, json=csd_data, auth=(username, password))

            # Manejar la respuesta de la API
            if response.status_code == 200:
                # Si se carga correctamente
                csd.is_uploaded = True  # Marcar cargado exitorsamente en Facturama
                csd.save()  # Ahora sí guardamos en la BD
                messages.success(request, 'CSD cargado correctamente.')
                return redirect('success')  # Redirigir a una página de éxito
            else:
                # Si ocurre un error, mostrar el mensaje
                error_message = f"Error al cargar CSD: {response.text}"
                messages.error(request, error_message)
                return render(request, 'facturacion/cargar_csd.html', {'form': form})
    else:
        form = CSDForm()
    return render(request, 'facturacion/cargar_csd.html', {'form': form})

def convertir_a_base64(file):
    return base64.b64encode(file.read()).decode('utf-8')

def success(request):
    return render(request, 'facturacion/success.html', {'message': 'CSD cargado exitosamente.'})

def CF(request):
    form = FacturaForm()
    cotizaciones = Cotizacion.objects.all()
    context = {
        'form': form,
        'cotizaciones': cotizaciones,
    }
    return render(request, "cotizaciones.html", context)
