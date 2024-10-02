from datetime import datetime, timedelta
import json
import os
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.http import  FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import requests
from accounts.helpers import get_unica_organizacion
from accounts.models import Cotizacion, OrdenTrabajo, OrdenTrabajoConcepto, Servicio
from facturacion.models import CSD, Factura
from .forms import CSDForm, CancelarCFDI, ComprobanteDePagoForm, FacturaEncabezadoForm, FacturaForm, FacturaPieForm, FacturaTotalesForm, ServicioFormset
from django.contrib import messages
import base64
import requests
from django.core.files.base import ContentFile
from django.conf import settings  # Asegúrate de tener tu configuración adecuada
from django.db.models import Max
from django.db import transaction

SANDBOX_URL = "https://apisandbox.facturama.mx"

now_utc = datetime.utcnow()# Obtener la hora UTC actual
offset = timedelta(hours=-8)  # Usa -7 si estás en horario de verano
now_tijuana = now_utc + offset

def buscar_cfdi_id( emisor_rfc,id):
    try:
        username = "AranzaInade"  # nombre de usuario
        password = "Puebla4990"
        # CONSTRUIR LA URL DEL ENDPOINT
        url = f"{SANDBOX_URL}/cfdi?type=issuedLite&rfcIssuer={emisor_rfc}&cfdiId={id}"
        
        response = requests.get(url, auth=(username, password))
        
        if response.status_code == 200:
            data=response.json()
            
            # Extraer todos los datos de factura
            folios = [factura['Folio'] for factura in data]
            
            if folios:
                # Convertir los datos a enteros para encontrar el mas grande
                folios_int = [int(folio) for folio in folios]
                # Obtener el folio mas grande
                mayor_folio = max(folios_int)
                # Generar el siguiente folio, incrementando el mayor por 1
                siguiente_folio = mayor_folio + 1
                # Formatear el siguiente folio como una cadena con ceros a la izquierda
                siguiente_folio_str = str(siguiente_folio).zfill(4)
                return siguiente_folio_str
            else:
                # Si no hay facturas, el siguiente folio sería 1
                    return '0001'
        else:
            # Manejar errores de la API
            print(f"Error al hacer la solicitud a la API: {response.status_code}")
            return redirect('error', message="Error en la solicitud a la API")
            
    except requests.RequestException as e:
        # Manejar errores de conexión o de la API
        print(f"Error al hacer la solicitud a la API: {e}")
        return redirect('error', message="Error en la solicitud a la API")

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
            
            # URL de la API de Facturama
            url = "https://apisandbox.facturama.mx/api-lite/csds"
            username = "AranzaInade"  # nombre de usuario
            password = "Puebla4990"
            response = requests.post(url, json=csd_data, auth=(username, password))

            # Manejar la respuesta de la API
            if response.status_code == 200:
                # Si se carga correctamente
                csd.is_uploaded = True  # Marcar cargado exitorsamente en Facturama
                csd.save()  # Ahora sí guardamos en la BD
                messages.success(request, 'CSD cargado correctamente.')
                # Redirigir a una página de éxito
                return redirect('cargar_csd')
            else:
                    # Si ocurre un error, intenta extraer un mensaje más claro
                try:
                    # Intenta cargar el contenido como JSON
                    error_data = response.json()
                    message = error_data.get("Message", "Error desconocido al cargar CSD.")
                    model_state = error_data.get("ModelState", {})
                    
                    # Construir un mensaje de error más detallado si hay información en ModelState
                    model_errors = []
                    for field, errors in model_state.items():
                        for error in errors:
                            model_errors.append(f"{field}: {error}")

                    # Combinar los mensajes
                    detailed_error = message + (" Detalles: " + "; ".join(model_errors) if model_errors else "")
                except (ValueError, KeyError):
                    # Si no es un JSON válido o faltan claves, mostrar el texto completo
                    detailed_error = response.text

                # Mostrar el mensaje de error
                messages.error(request, f"Error al cargar CSD: {detailed_error}")
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

def facturas_list(request):
    context ={
        'facturas' :  Factura.objects.all()
    }
    return render (request, "facturacion/facturas.html",context)

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

@login_required
@transaction.atomic
def crear_factura(request, id_personalizado):
    
# Obtener la orden de trabajo
    orden = OrdenTrabajo.objects.get(id_personalizado=id_personalizado)
    cliente = orden.cotizacion.persona
    emisor = orden.cotizacion.usuario
    conceptos = OrdenTrabajoConcepto.objects.filter(orden_de_trabajo=id_personalizado)

    if request.method == 'POST':
        
        encabezado_form = FacturaEncabezadoForm(request.POST, initial={'orden': orden.id_personalizado})
        pie_form = FacturaPieForm(request.POST, initial={'direccion': orden.direccion})
        totales_form = FacturaTotalesForm(request.POST)
        
        if encabezado_form.is_valid() and pie_form.is_valid() and totales_form.is_valid():

            # Obteniendo datos de formularios
            datos_e = encabezado_form.cleaned_data
            datos_p = pie_form.cleaned_data
            datos_t = totales_form.cleaned_data
            
            # Intentar obtener el CSD de la organización
            try:
                organizacion = orden.cotizacion.usuario.organizacion
                csd = CSD.objects.get(organizacion=organizacion)
            except CSD.DoesNotExist:
                messages.error(request, "No se encontró un CSD asociado a la organización. Por favor, cargue un CSD de manera correcta antes de continuar.")
                context = {
                    'orden': orden,
                    'cliente': cliente,
                    'encabezado_form': encabezado_form,
                    'pie_form': pie_form,
                    'totales_form': totales_form,
                    'conceptos': conceptos,
                }
                return render(request, 'facturacion/formulario.html', context)
            
            # Obtener el último ID existente
            el_id = Factura.objects.aggregate(Max('id'))['id__max']
            emisor_rfc = csd.rfc
            siguiente_id_formateado = buscar_cfdi_id( emisor_rfc ,el_id)
            # Imprimir o utilizar el siguiente ID
            print(f"El siguiente ID será: {siguiente_id_formateado}")

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

            tipo_moneda = datos_e['tipo_moneda']
            orden_compra = datos_e['OrderNumber']
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
                codigo_servicio = request.POST.get(f'concepto.concepto.servicio.codigo_{i}')
                nombre_servicio = request.POST.get(f'nombre_servicio_{i}')
                metodo = request.POST.get(f'metodo_{i}')
                cantidad_servicios = request.POST.get(f'cantidad_servicios_{i}')
                precio = request.POST.get(f'precio_{i}')
                importe = request.POST.get(f'importe_{i}')

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
                                'id': servicio.codigo,
                                'codigo': servicio.clave_cfdi,  # Código CFDI que es el que necesita el SAT
                                'nombre': servicio.nombre_servicio,  # Nombre del servicio
                                'unit': servicio.unidad,
                                'unit_cfdi': servicio.unidad_cfdi,
                                'precio': precio,  # Precio unitario del servicio
                                'metodo': servicio.metodo,  # Método asociado al servicio
                                'cantidad': cantidad_servicios,  # Cantidad de servicios
                                'objeto_imp': servicio.objeto_impuesto,
                                'importe': importe  # Importe total para ese servicio
                            })
                    except Servicio.DoesNotExist:
                        # Si el servicio no existe, podrías lanzar una excepción o manejar el error de otra forma
                        raise ValueError(f"El servicio con el código {codigo_servicio} no existe.")

            cfdi_data = {
                # "CfdiType":"I"
                # ( integer ) Atributo para especificar el nombre que se establecera en el pdf (default 1 = factura) [ Vea la documentación de "Nombres del CFDI" ]
                "NameId": "1",
                # ( Strg )Tipo de cambio de la moneda en caso de ser diferente de MXN
                "Currency": "MXN",
                # ( string ) Folio: Atributo para control interno del contribuyente que expresa el folio del comprobante, acepta una cadena de 1 a 40 caracteres.
                "Folio": siguiente_id_formateado,
                "Date": now_tijuana.isoformat(),  # Fecha actual en formato ISO 8601
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
                        "IdProduct": concepto['id'],
                        "ProductCode": concepto['codigo'],
                        "Description": concepto['nombre'],
                        "Unit": concepto['unit'],
                        "UnitCode": concepto['unit_cfdi'],
                        "UnitPrice": float(concepto['precio']),
                        "Quantity": float(concepto['cantidad']),
                        "Subtotal": float(concepto['importe']),
                        "TaxObject": concepto['objeto_imp'],
                        "Taxes": [
                            {
                                "Total": float(concepto['importe']) * 0.16,
                                "Name": "IVA",
                                "Base": float(concepto['importe']),
                                "Rate": 0.16,
                                "IsRetention": False
                            }
                        ],
                        "Total": round(float(concepto['importe']) * 1.16, 2)
                    }
                    for concepto in conceptos_data
                ]
            }
            print(cfdi_data)
            # URL de la API de Facturama
            url = "https://apisandbox.facturama.mx/api-lite/3/cfdis"
            username = "AranzaInade"  # nombre de usuario
            password = "Puebla4990"
            response = requests.post(url, json=cfdi_data, auth=(username, password))

            # Manejar la respuesta de la API
            if response.status_code == 201:
                # Si se carga correctamente
                response_data = response.json()
                # Imprime la respuesta
                print(json.dumps(response_data, indent=4))
                resp = json.dumps(response_data, indent=4)
                # Extrae el "Id"
                cfdi_id = response_data.get("Id")
                print(f"El ID del CFDI es: {cfdi_id}")
                messages.success(request, 'CFDI timbrado correctamente.')
                print(request , messages)
                print("Guardando en la BD")

                
                # Guarda factrura en la BD
                nueva_factura = Factura(
                    # Aquí debes agregar los campos necesarios para la factura
                    id=response_data.get("Folio"),
                    cfdi_id=response_data.get("Id"),
                    cfdi_type = response_data.get("CfdiType"),
                    Type = response_data.get("Type"),
                    orden=orden,
                    OrderNumber=orden_compra,
                    cliente=cliente,
                    emisor=emisor.organizacion,
                    forma_pago=response_data.get("PaymentTerms"),
                    metodo_pago=response_data.get("PaymentMethod"),
                    ExpeditionPlace = response_data.get("ExpeditionPlace"),
                    ExchangeRate = response_data.get("ExchangeRate"),
                    tipo_moneda=orden.cotizacion.metodo_pago,#tipo_moneda=tipo_moneda,
                    subtotal=response_data.get("Subtotal"),
                    tasa_iva = datos_t['tasa_iva'],
                    Discount = response_data.get("Discount"),
                    iva=datos_t['iva'],
                    total=response_data.get("Total"),
                    comentarios=response_data.get("Observations"),
                    correos=correos,
                    estado=response_data.get("Status"),
                    OriginalString=response_data.get("OriginalString"),
                    CfdiSign=response_data.get("Complement", {}).get("TaxStamp", {}).get("CfdiSign"),
                    SatSign=response_data.get("Complement", {}).get("TaxStamp", {}).get("SatSign"),
                )
                nueva_factura.save() # Asegúrate de guardar la factura
                # verificar si con la API se puede crear o manejar los <comprobantes de pagos
                
                
                
                # Redirigir a una página de éxito
                return redirect('home')
            else:
                # Si ocurre un error, mostrar un mensaje detallado
                error_code = response.status_code
                error_message = response.json().get("message", "Ocurrió un error inesperado.")
                full_error_message = f"Error al cargar CSD. Código: {error_code}. Mensaje: {error_message}. Detalles: {response.text}"
                messages.error(request, full_error_message)
                print(request, full_error_message)
            
        # Aquí envías `cfdi_data` a la API de Facturama utilizando tu cliente HTTP (requests u otro)

        return redirect('home')
    
    encabezado_form = FacturaEncabezadoForm(initial={'orden': orden.id_personalizado, 'tipo_moneda': orden.cotizacion.metodo_pago})
    pie_form = FacturaPieForm(initial={'direccion': orden.direccion,'comentarios': orden.cotizacion.notas, 'correos': orden.cotizacion.correos_adicionales})
    totales_form = FacturaTotalesForm()
    
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
def generar_factura_xml(request, id_factura):
    factura = get_object_or_404(Factura, cfdi_id=id_factura)

    # Verificar si ya existe un archivo XML asignado
    if not factura.xml_file:
        # Construir la URL del endpoint para obtener el XML
        url = f"https://apisandbox.facturama.mx/cfdi/xml/issuedLite/{id_factura}"
        username = "AranzaInade"  # nombre de usuario
        password = "Puebla4990"

        # Solicitud al API de Facturama
        response = requests.get(url, auth=(username, password))

        # Manejar una respuesta API
        if response.status_code == 200:
            # Recuperar XML de response
            xml_content = response.content

            # Guardar el archivo XML en la carpeta media/facturas/
            factura.xml_file.save(f'factura_{id_factura}.xml', ContentFile(xml_content))

            # Guardar cambios en la instancia
            factura.save()
            messages.success(request, "XML generado y asignado correctamente.")
            return redirect('factura_detalle', cfdi_id=id_factura)  # Redirige al detalle
        else:
            # Manejar el error si no se pudo obtener el XML
            error_code = response.status_code
            error_message = response.json().get("message", "Ocurrió un error inesperado.")
            full_error_message = f"Error al cargar CSD. Código: {error_code}. Mensaje: {error_message}. Detalles: {response.text}"
            messages.error(request, full_error_message)
            print(full_error_message)
            return redirect('factura_detalle', cfdi_id=id_factura)

    elif factura.xml_file:
        # Retornamos el archivo XML guardado para descargar
        response = FileResponse(factura.xml_file.open(), content_type='application/xml')
        response['Content-Disposition'] = f'attachment; filename="factura_{id_factura}.xml"'
        return redirect('factura_detalle', cfdi_id=id_factura)  # Redirige al detalle

    else:
        raise Http404("El archivo XML no se encuentra.")

@login_required
def generar_factura_pdf(request,id_factura):
    factura = get_object_or_404(Factura, cfdi_id=id_factura)
    
    # Verificar si ya existe un archivo PDF asignado
    if not factura.pdf_file:
    
        # Construir la URL del endpoint
        url = f"https://apisandbox.facturama.mx/cfdi/pdf/issuedLite/{id_factura}"
        username = "AranzaInade"  # nombre de usuario
        password = "Puebla4990"
        # Solicitud al API de Facturama
        response = requests.get(url, auth=(username, password))
        
        # Manejar una respuesta API 
        if response.status_code == 200:
            
            # Recuperar pdf de response
            response_data = response.json()
            pdf_content = base64.b64decode(response_data.get("Content"))
            
            # Guardar el archivo PDF en la carpeta media/facturas/
            factura.pdf_file.save(f'factura_{id_factura}.pdf', ContentFile(pdf_content))
            
            # Guardar cambios en la instancia
            factura.save()
            messages.success(request, "PDF generado y asignado correctamente.")
            return redirect('factura_detalle', cfdi_id=id_factura)  # Redirige a la vi
        else:
            
            # Manejar el error si no se pudo obtener el PDF
            error_code = response.status_code
            error_message = response.json().get("message", "Ocurrió un error inesperado.")
            full_error_message = f"Error al cargar CSD. Código: {error_code}. Mensaje: {error_message}. Detalles: {response.text}"
            messages.error(request, full_error_message)
            print(request, full_error_message)
            # Renderizar el template de error
            return redirect('factura_detalle', cfdi_id=id_factura)
           
    elif factura.pdf_file:
        # Retornamos el archivo PDF guardado
        return FileResponse(factura.pdf_file.open(), content_type='application/pdf')
    
    else:
        
        raise Http404("El archivo PDF no se encuentra.")
    
@login_required
def factura_detalle(request, cfdi_id):
    
    factura = get_object_or_404(Factura, cfdi_id=cfdi_id)
    
    form_cancel = CancelarCFDI(initial={'cfdi_id': factura.cfdi_id})
    form_comprobante = ComprobanteDePagoForm(initial={'Amount':factura.total,'OperationNumber':factura.id,'ForeignAccountNamePayer':factura.cliente.empresa.nombre_empresa,'RfcReceiverBeneficiaryAccount':factura.cliente.empresa.rfc})
    
    context = {
        'factura' : factura,
        'id': f'{factura.id:04}',
        'form_cancel': form_cancel,
        'form_comprobante': form_comprobante,
    }
    
    return render(request, 'facturacion/factura_detalle.html', context)

def cancelar_factura(request):
    
    if request.method == 'POST':
        form_cancel = CancelarCFDI(request.POST)
        
        if form_cancel.is_valid():
            # Obteniendo datos del formulario
            motive = form_cancel.cleaned_data['motive']
            uuid_replacement = form_cancel.cleaned_data.get('uuid_replacement')  # uuid_replacement podría ser opcional
            cfdi_id = form_cancel.cleaned_data['factura_id']
            
            # Llama a la función para cancelar la factura
            success, response = cancelar_factura_api(cfdi_id, motive, uuid_replacement)
            
            if success:
                messages.success(request, "Factura cancelada exitosamente.")
            else:
                messages.error(request, f"Error al cancelar la factura: {response}")
            
            return redirect('factura_detalle', cfdi_id=cfdi_id)
        else:
            cfdi_id = request.POST.get('factura_id')
            messages.error(request, "Error en el formulario")
            return redirect('factura_detalle', cfdi_id=cfdi_id)
            
def cancelar_factura_api(factura_id, motive, uuid_replacement):
    url = f"https://apisandbox.facturama.mx/api-lite/cfdis/{factura_id}?motive={motive}&uuidReplacement={uuid_replacement}"
    
    # Realiza la llamada a la API (usa el método que necesites, por ejemplo POST)
    try:
        username = "AranzaInade"  # nombre de usuario
        password = "Puebla4990"
        # Solicitud al API de Facturama
        response = requests.delete(url, auth=(username, password))
        if response.status_code == 200:
            # La solicitud fue exitosa
            factura = get_object_or_404(Factura, cfdi_id=factura_id)
            factura.estado = 'canceled'
            factura.save()  # Asegúrate de guardar los cambios en la base de datos
            return True, response.json()  # Puedes devolver la respuesta en JSON si lo necesitas
        else:
            # Manejo de errores
            return False, response.json()  # Puedes devolver el mensaje de error
    except requests.exceptions.RequestException as e:
        # Manejo de excepciones
        return False, str(e) 
    
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages

def comprobante_factura(request, cfdi_id):
    # Asignar ID
    factura = get_object_or_404(Factura, cfdi_id=cfdi_id)
    
    if request.method == 'POST':
        form_comprobante = ComprobanteDePagoForm(request.POST)
        
        if form_comprobante.is_valid():
            
            # Intentar obtener el CSD de la organización
            try:
                organizacion = factura.emisor
                csd = CSD.objects.get(organizacion=organizacion)
            except CSD.DoesNotExist:
                messages.error(request, "No se encontró un CSD asociado a la organización. Por favor, cargue un CSD de manera correcta antes de continuar.")
                return redirect('facturas_list')
            
            # Obtener Datos
            date = form_comprobante.cleaned_data.get('Date')
            paymentform = form_comprobante.cleaned_data.get('PaymentForm')
            amount = form_comprobante.cleaned_data.get('Amount')
            operationnumber = form_comprobante.cleaned_data.get('OperationNumber')
            ForeignAccountNamePayer = form_comprobante.cleaned_data.get('ForeignAccountNamePayer')
            PayerAccount = form_comprobante.cleaned_data.get('PayerAccount')
            RfcReceiverBeneficiaryAccount = form_comprobante.cleaned_data.get('RfcReceiverBeneficiaryAccount')
            BeneficiaryAccount = form_comprobante.cleaned_data.get('BeneficiaryAccount')
            
            el_id = Factura.objects.aggregate(Max('id'))['id__max']
            emisor_rfc = csd.rfc
            siguiente_id_formateado = buscar_cfdi_id( emisor_rfc ,el_id)
            print(f"El siguiente ID será: {siguiente_id_formateado}")

            # Construir el JSON para la API de Facturama
            complemento_pago = {
                "NameId": "14",  # Se aplica 14 para complemento de pago
                "Folio": siguiente_id_formateado,  # Asegúrate de que esta variable tenga valor
                "Serie": "COP",
                "CfdiType": "P",
                "OrderNumber": str(factura.orden.id_personalizado),
                "ExpeditionPlace": factura.ExpeditionPlace,
                "Date": now_tijuana.isoformat(),  # Formato correcto
                "Observations": "Comprobante de pago",
                "LogoUrl": organizacion.logo,
                "Exportation": "01",
                "Issuer": { # Nodo Issuer sólo necesario si se usa API Multiemisor
                    "Rfc": emisor_rfc,
                    "Name": factura.emisor.nombre,
                    "FiscalRegime": factura.emisor.regimen_fiscal
                },
                "Receiver": {
                    "Rfc": factura.cliente.empresa.rfc,
                    "CfdiUse": "CP01",
                    "Name": factura.cliente.empresa.nombre_empresa,
                    "FiscalRegime": factura.cliente.empresa.regimen_fiscal,
                    "TaxZipCode": factura.cliente.empresa.direccion.codigo
                },
                "Complemento": {
                    "Payments": [
                        {
                            "Date": date.isoformat(),
                            "PaymentForm": paymentform,
                            "Amount": amount,
                            "OperationNumber": operationnumber, # Número de operación
                            "RfcIssuerPayerAccount": emisor_rfc, # RFC Emisor Ordenante
                            "ForeignAccountNamePayer": ForeignAccountNamePayer, # Nombre Ordenante
                            "PayerAccount": PayerAccount, # Cuenta Ordenante
                            "RfcReceiverBeneficiaryAccount": RfcReceiverBeneficiaryAccount, # RFC beneficiario
                            "BeneficiaryAccount": BeneficiaryAccount, # Nombre beneficiario
                            "RelatedDocuments": [
                                # {
                                #     "TaxObject": "02",
                                #     "Uuid": "23361131-a0e0-4cf6-85d3-47f37679e874",
                                #     "PartialityNumber": "1",
                                #     "Serie": "1111",
                                #     "Folio": "45",
                                #     "Currency": "MXN",
                                #     "PaymentMethod": "PPD",
                                #     "PreviousBalanceAmount": "111.75",
                                #     "AmountPaid": "111.75",
                                #     "ImpSaldoInsoluto": "0",
                                #     "Taxes": [
                                #         {
                                #             "Name": "IVA",
                                #             "Rate": "0.16",
                                #             "Total": "16",
                                #             "Base": "100",
                                #             "IsRetention": "false"
                                #         }
                                #     ]
                                # }
                            ]
                        }
                    ]
                }
            }
                    
                    
            print(complemento_pago)
            # Aquí, agrega la lógica para enviar `complemento_pago` a la API de Facturama.
            
            # Después de procesar, redirige o renderiza la respuesta adecuada.
            messages.success(request, "Comprobante de pago generado exitosamente.")
            return redirect('facturas_list')  # Redirige a donde necesites

        else:
            print(form_comprobante.errors)
            messages.error(request, f"Error al generar comprobante de pago. {form_comprobante.errors}")
            return redirect('facturas_list')  # También puedes optar por volver a mostrar el formulario aquí
    else:
        form_comprobante = ComprobanteDePagoForm()  # Crea una instancia del formulario si no es POST

    # Renderiza el template si es un GET
    return render(request, 'tu_template.html', {'form_comprobante': form_comprobante, 'factura': factura})

      
def comprobar_pago_factura_api(request, cfdi_id):
    
    if request.method == 'POST':
        factura = get_object_or_404(Factura, cfdi_id=cfdi_id)
        
        payment_date = request.POST.get('payment_date')
        
    context = {
        'factura' : factura,
        'id': f'{factura.id:04}',
    }
    return render(request, 'facturacion/comprobar_pago.html', context)