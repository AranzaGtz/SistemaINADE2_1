from datetime import datetime
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from accounts.forms import AlmacenForm, SucursalForm
from accounts.helpers import get_unica_organizacion
from accounts.models import Cotizacion, OrdenTrabajo, OrdenTrabajoConcepto, Organizacion, Servicio
from facturacion.models import CSD, Factura
from .forms import CSDForm, FacturaEncabezadoForm, FacturaForm, FacturaPieForm, FacturaTotalesForm, ServicioFormset
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


def agregar_almacen(request):
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
    # Buscar orden de trabajo
    orden = get_object_or_404(OrdenTrabajo, id_personalizado=id_personalizado)
    cliente = orden.cotizacion.persona
    emisor = orden.cotizacion.usuario

    # Buscar conceptos de la orden de trabajo
    conceptos = OrdenTrabajoConcepto.objects.filter(
        orden_de_trabajo=id_personalizado)

    # En este caso inicializamos los formularios vacios
    encabezado_form = FacturaEncabezadoForm(
        initial={'orden': orden.id_personalizado, 'tipo_moneda': orden.cotizacion.metodo_pago})
    pie_form = FacturaPieForm(initial={'direccion': orden.direccion,
                              'comentarios': orden.cotizacion.notas, 'correos': orden.cotizacion.correos_adicionales})
    totales_form = FacturaTotalesForm()
    servicio_formset = ServicioFormset()

    if request.method == 'POST':
        print("Facturando...")
        # Inicializamos los formularios con POST
        encabezado_form = FacturaEncabezadoForm(
            request.POST, initial={'orden': orden.id_personalizado})
        pie_form = FacturaPieForm(request.POST, initial={
                                  'direccion': orden.direccion})
        totales_form = FacturaTotalesForm(request.POST)
        print("Validando formularios...")

        if encabezado_form.is_valid() and pie_form.is_valid() and totales_form.is_valid():

            # Obteniendo datos de formularios
            datos_e = encabezado_form.cleaned_data
            datos_p = pie_form.cleaned_data
            datos_t = totales_form.cleaned_data

            # Puedes acceder a los datos así
            organizacion = orden.cotizacion.usuario.organizacion
            csd = get_object_or_404(CSD, organizacion=organizacion)

            cliente_rfc = request.POST.get('id_cliente_rfc')
            cliente_regimen = request.POST.get('id_cliente_reg')
            cliente_nombre = request.POST.get('id_cliente_nombre')
            cliente_cp = cliente.empresa.direccion.codigo
            cliente_calle = cliente.empresa.direccion.calle
            cliente_colonia = cliente.empresa.direccion.colonia
            cliente_ciudad = cliente.empresa.direccion.ciudad
            cliente_estado = cliente.empresa.direccion.estado

            emisor_rfc = csd.rfc
            emisor_nombre = emisor.organizacion.nombre
            emisor_regimen = emisor.organizacion.regimen_fiscal
            emisor_cp = emisor.organizacion.direccion.codigo

            sucursal = datos_e['sucursal']
            almacen = datos_e['almacen']
            tipo_moneda = datos_e['tipo_moneda']
            orden_compra = datos_e['orden_compra']
            uso_cfdi = datos_e['uso_cfdi']
            forma_pago = datos_e['forma_pago']
            metodo_pago = datos_e['metodo_pago']
            direccion = datos_p['direccion']
            comentarios = datos_p['comentarios']
            notificacion = datos_p['notificacion']
            correos = datos_p['correos']
            subtotal = datos_t['subtotal']
            iva = datos_t['iva']
            tasa_iva = datos_t['tasa_iva']
            total = datos_t['total']

            # Iteramos sobre los conceptos
            conceptos_data = []
            # Suponiendo que el contador empieza en 1 y termina en el último concepto
            for i in range(1, len(request.POST) + 1):
                # Obtenemos los datos de cada concepto desde el formulario
                codigo_servicio = request.POST.get(
                    f'concepto.concepto.servicio.codigo_{i}')
                nombre_servicio = request.POST.get(f'nombre_servicio_{i}')
                metodo = request.POST.get(f'metodo_{i}')
                cantidad_servicios = request.POST.get(
                    f'cantidad_servicios_{i}')
                precio = request.POST.get(f'precio_{i}')
                importe = request.POST.get(f'importe_{i}')

                servicio = get_object_or_404(Servicio, codigo=codigo_servicio)

                # Buscamos el servicio en la base de datos a partir del código
                if codigo_servicio:
                    try:
                        servicio = Servicio.objects.get(codigo=codigo_servicio)

                        # Verificamos si existen valores para el servicio y la cantidad
                        if servicio and cantidad_servicios:
                            # Convertimos a float si es necesario
                            cantidad_servicios = float(cantidad_servicios)
                            precio_unitario = float(servicio.precio_unitario)
                            importe = precio_unitario * cantidad_servicios

                            # Agregamos los datos del servicio a conceptos_data
                            conceptos_data.append({
                                'codigo': servicio.clave_cfdi,  # Código CFDI que es el que necesita el SAT
                                'nombre': servicio.nombre_servicio,  # Nombre del servicio
                                'metodo': servicio.metodo,  # Método asociado al servicio
                                'cantidad': cantidad_servicios,  # Cantidad de servicios
                                'precio': precio_unitario,  # Precio unitario del servicio
                                'importe': importe  # Importe total para ese servicio
                            })
                    except Servicio.DoesNotExist:
                        # Si el servicio no existe, podrías lanzar una excepción o manejar el error de otra forma
                        raise ValueError(f"El servicio con el código {codigo_servicio} no existe.")

            # Verificamos si existen valores para el índice actual
            if codigo_servicio and nombre_servicio:
                conceptos_data.append({
                    'codigo': codigo_servicio,
                    'nombre': nombre_servicio,
                    'metodo': metodo,
                    'cantidad': cantidad_servicios,
                    'precio': precio,
                    'importe': importe
                })

            cfdi_data = {
                # "CfdiType":"I"
                # ( integer ) Atributo para especificar el nombre que se establecera en el pdf (default 1 = factura) [ Vea la documentación de "Nombres del CFDI" ]
                "NameId": "1",
                # ( Strg )Tipo de cambio de la moneda en caso de ser diferente de MXN
                "Currency": "MXN",
                # ( string ) Folio: Atributo para control interno del contribuyente que expresa el folio del comprobante, acepta una cadena de 1 a 40 caracteres.
                "Folio": "1",
                "Date": datetime.now().isoformat(),  # Fecha actual en formato ISO 8601
                # ( string ) Atributo requerido para expresar el efecto del comprobante fiscal para el contribuyente emisor: ingreso, egreso ó traslado Required Data type: TextMatching regular expression pattern: I|E|T|N|P
                "CfdiType": "I",
                # ( string ) Url del logo, ej. https://dominio.com/mi-logo.png
                "LogoUrl": "",
                # ( string ) Atributo obligatorio y de catálogo, para expresar la forma de pago de los bienes o servicios amparados por el comprobante. Se entiende como método de pago leyendas tales como: 01, 02, 03, 99
                "PaymentForm": forma_pago,
                # ( string ) Atributo obligatorio y de catálogo, para expresar el método de pago de los bienes o servicios amparados por el comprobante. Se entiende como método de pago leyendas tales como: PPD, PUE
                "PaymentMethod": metodo_pago,
                # ( string ) Lugar de Expedición (Codigo Postal desde donde se expide el comprobante)
                "ExpeditionPlace": emisor_cp,
                # ( string ) Descripcion no fiscal del pdf
                "Observations": comentarios,
                # ( string ) Numero de Orden, propiedad no fiscal (opcional)Max length: 100
                "OrderNumber": orden_compra,

                "Issuer": {  # ( TaxEntityInfoViewModel ) Nodo que contiene el detalle del emisor.
                    "Rfc": emisor_rfc,
                    "Name": emisor_nombre,
                    "FiscalRegime": emisor_regimen
                },

                "Receiver": {  # Receiver ( ReceiverV4BindingModel ) Cliente a quien se emitirá el CFDi, Atributo Requerido
                    # No se cual es el CFDI use, hay que buscarlo en la Bd si no hay que agregarlo
                    "Rfc": cliente_rfc,
                    "Name": cliente_nombre,
                    "CfdiUse": uso_cfdi,
                    "FiscalRegime": cliente_regimen,
                    "TaxZipCode": cliente_cp,

                    "Address": {
                        "Street": cliente_calle,
                        "Neighborhood": cliente_colonia,
                        "ZipCode": cliente_cp,
                        "Municipality": cliente_ciudad,
                        "State": cliente_estado,
                        "Country": "MEX"
                    }
                },
                "Items": [
                    {
                        "ProductCode": concepto['codigo'],
                        "Description": concepto['nombre'],
                        "Unit": "E48",
                        "UnitCode": "E48",
                        "UnitPrice": float(concepto['precio']),
                        "Quantity": float(concepto['cantidad']),
                        "Subtotal": float(concepto['importe']),
                        "Taxes": [
                            {
                                "Total": float(concepto['importe']) * 0.16,
                                "Name": "IVA",
                                "Base": float(concepto['importe']),
                                "Rate": 0.16,
                                "IsRetention": False
                            }
                        ],
                        "Total": float(concepto['importe']) * 1.16
                    }
                    for concepto in conceptos_data
                ]
            }

            # # URL de la API de Facturama
            # url = "https://apisandbox.facturama.mx/api-lite/3/cfdis"
            # username = "AranzaInade"  # nombre de usuario
            # password = "Puebla4990"
            # response = requests.post(
            #     url, json=cfdi_data, auth=(username, password))

            # # Manejar la respuesta de la API
            # if response.status_code == 201:
            #     # Si se carga correctamente
            #     messages.success(request, 'CFDI timbrado correctamente.')
            #     print(messages, error_message)
            #     # Redirigir a una página de éxito
            #     return redirect('home')
            # else:
            #     # Si ocurre un error, mostrar el mensaje
            #     error_message = f"Error al cargar CSD: {response.text}"
            #     messages.error(request, error_message)
            #     print(error_message)
        print(cfdi_data)
        # Aquí envías `cfdi_data` a la API de Facturama utilizando tu cliente HTTP (requests u otro)

        return redirect('home')
    context = {
        'orden': orden,
        'cliente': cliente,
        'encabezado_form': encabezado_form,
        'pie_form': pie_form,
        'totales_form': totales_form,
        'conceptos': conceptos,
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

            # Obtener la organización seleccionada en el formulario
            # El formulario incluiría un campo para seleccionar la organización
            organizacion = get_unica_organizacion()

            # Asignar la única organización automáticamente
            csd.organizacion = organizacion

            # Guardar los archivos, rfc y contraseña del formulario
            rfc = form.cleaned_data['rfc']
            cer_file = form.cleaned_data['cer_file']
            key_file = form.cleaned_data['key_file']
            key_password = form.cleaned_data['password']

            # Convertir los archivos a base64
            cer_base64 = convertir_a_base64(cer_file)
            key_base64 = convertir_a_base64(key_file)

            # Preparar los datos para el API de Facturama
            csd_data = {
                "Rfc": rfc,
                "Certificate": cer_base64,
                "PrivateKey": key_base64,
                "PrivateKeyPassword": key_password,
            }

            print(csd_data)

            # URL de la API de Facturama
            url = "https://apisandbox.facturama.mx/api-lite/csds"
            username = "AranzaInade"  # nombre de usuario
            password = "Puebla4990"
            response = requests.post(
                url, json=csd_data, auth=(username, password))

            # Manejar la respuesta de la API
            if response.status_code == 200:
                # Si se carga correctamente
                csd.is_uploaded = True  # Marcar cargado exitorsamente en Facturama
                csd.save()  # Ahora sí guardamos en la BD
                messages.success(request, 'CSD cargado correctamente.')
                # Redirigir a una página de éxito
                return redirect('cargar_csd')
            else:
                # Si ocurre un error, mostrar el mensaje
                error_message = f"Error al cargar CSD: {response.text}"
                messages.error(request, error_message)
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
