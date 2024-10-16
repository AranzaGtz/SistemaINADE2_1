# Importaciones estándar de Python
from datetime import datetime
from decimal import Decimal
import os
from django.core.mail import EmailMessage
import json
import base64

# Importaciones de bibliotecas de terceros
import requests
import pytz

# Importaciones de Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

# Importaciones de tu proyecto
from SistemaINADE2.settings import EMAIL_HOST_USER, PASSWORD, SANDBOX_URL, USERNAME
from accounts.helpers import get_unica_organizacion
from accounts.models import Cotizacion, OrdenTrabajo, OrdenTrabajoConcepto, Servicio
from facturacion.models import CSD, Comprobante, Factura
from .forms import (CSDForm, CancelarCFDI, ComprobantePagoForm, EmailForm, FacturaEncabezadoForm, FacturaForm, FacturaPieForm, FacturaTotalesForm)

# Obtener la zona horaria UTC
utc_timezone = pytz.UTC

# Obtener la fecha y hora actual en UTC
aware_datetime = datetime.now(utc_timezone)  # Ahora ya es un datetime "aware"

# ------------------------------- #
#   FUNCIONES
# ------------------------------- #

def get_emisor(request): #   FUNCION PARA ENCONTRAR EL RFC PARA INDICAR EMISOR EN API  
    try:
        if not request.user.is_authenticated:
            messages.error(request, "Debe iniciar sesión para acceder a esta función.")
            return redirect('login')
            
        user_log = request.user
        
        if not hasattr(user_log, 'organizacion'):
            messages.error(request, "No se encuentra el RFC de la organización por medio del usuario logueado.")
            return redirect('home')
        
        org = user_log.organizacion
        csd = get_object_or_404(CSD, organizacion = org)
        rfc = csd.rfc
        return rfc
    except Exception as e:
        # Capturamos cualquier otro error no esperado y lo mostramos
        messages.error(request, "No se encuentra el RFC de la organización por medio del usuario logueado.")
        return redirect('home')  # Redirige a la vista 'home'

def buscar_cfdi_return(id): #   FUNCION PARA BUSCAR EL CFDI Y REGRESARLO
    try:
        
        response = search_cfdi_return(id)
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Convertir la respuesta JSON a un diccionario de Python
            data = response.json()
            
            # Acceder a información específica
            uuid = data.get("Complement", {}).get("TaxStamp", {}).get("Uuid", "UUID no encontrado")
            folio = data.get("Folio", "Folio no encontrado")
            total = data.get("Total", "Total no encontrado")
            issuer_rfc = data.get("Issuer", {}).get("Rfc", "RFC del emisor no encontrado")

            return {
                "uuid": uuid,
                "folio": folio,
                "total": total,
                "issuer_rfc": issuer_rfc
            }
        else:
            print(f"Error en la solicitud: Código de estado {response.status_code}")
            return None
    except requests.RequestException as e:
        # Manejar errores de conexión o de la API
        print(f"Error al hacer la solicitud a la API: {e}")
        return None

def buscar_cfdi_id( emisor_rfc,id): #   FUNCION PARA BUSCAR EL FOLIO DEL CFDI DEL EMISOR
    try:

        # CONSTRUIR LA URL DEL ENDPOINT
        url = f"{SANDBOX_URL}/cfdi?type=issuedLite&rfcIssuer={emisor_rfc}&cfdiId={id}%status=all"
        
        response = requests.get(url, auth=(USERNAME, PASSWORD))
        
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

def get_new_cfdi_id(): # FUNCION PARA BUSCAR EL SIGUIENTE NUEVO FOLIO DE LA BD
    # Lógica para obtener el siguiente ID en la base de datos
    last_factura = Factura.objects.order_by('id').last()
    
    if last_factura:
        next_id = int(last_factura.id) + 1
    else:
        next_id = 1
    
    return next_id

def get_new_cfdi_comp_id(): # FUNCION PARA BUSCAR EL SIGUIENTE NUEVO FOLIO DE UN COMPROBANTE DE PAGO DE LA BD
    # Lógica para obtener el siguiente ID en la base de datos
    last_comprobante = Comprobante.objects.order_by('folio').last()
    
    if last_comprobante:
        next_id = int(last_comprobante.folio) + 1
    else:
        next_id = 1
    print (f"{next_id:04d}")

def convertir_a_base64(file):
    return base64.b64encode(file.read()).decode('utf-8')

def success(request):
    return render(request, 'facturacion/success.html', {'message': 'CSD cargado exitosamente.'})

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
def facturas_list(request):
    emisor_rfc = get_emisor(request)
    cdfis_json = cfdis_all(emisor_rfc)

    # Ordenar facturas de forma descendente por la fecha de creación (o el campo que uses para este propósito)
    facturas = Factura.objects.all().order_by('-id')  # Asegúrate de que 'created_at' sea un campo válido en tu modelo

    context = {
        'facturas': facturas,
        'cdfis': cdfis_json,
    }
    return render(request, "facturacion/facturas.html", context)

@login_required
def factura_detalle(request, cfdi_id):
    
    factura = get_object_or_404(Factura, cfdi_id=cfdi_id)
    comprobantes = factura.comprobantes.all()
    form_cancel = CancelarCFDI(initial={'cfdi_id': factura.cfdi_id})
    form = ComprobantePagoForm(initial={
            'Amount': factura.total,
            'OperationNumber': factura.id,
            'ForeignAccountNamePayer': factura.cliente.empresa.nombre_empresa,
            'RfcReceiverBeneficiaryAccount': factura.cliente.empresa.rfc
        })
    form_send_email = EmailForm()
 
    response = search_cfdi_return(factura.cfdi_id)
    # Convertir la respuesta JSON a un diccionario de Python
    data = response.json()
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        
        # Acceder a información específica
        Receiver = data.get('Receiver',{})
        items = data.get('Items', [])  # Lista de items
        Taxes = data.get('Taxes',[])

        context = {
            'factura' : factura,
            'id': f'{factura.id:04}',
            'comprobantes': comprobantes,
            'form_cancel': form_cancel,
            'form' : form,
            'form_email': form_send_email,
            'items': items,
            'Receiver':Receiver,
            'data': data,
            'Taxes': Taxes,
        }
        
        return render(request, 'facturacion/factura_detalle.html', context)
    else:
        print(f"Error en la solicitud: Código de estado {response.status_code}")
        return JsonResponse({'success': False, 'status': response.status_code, 'data':data})

def create_and_save_fac (cfdi, file_type, id_factura):
    
    response = get_cfdi_doc(file_type, id_factura)  # Llama a la función que obtiene el documento
    
    if response.status_code != 200:
        raise Exception(f"No se pudo descargar el {file_type.upper()}.")
    
    # Decodificar el JSON de la respuesta
    response_json = response.json()

    # Verifica que el campo 'Content' esté presente
    if 'Content' not in response_json:
        raise Exception("La respuesta no contiene el contenido esperado.")

    # Extraer y decodificar el contenido Base64
    file_base64 = response_json['Content']
    file_content = base64.b64decode(file_base64)  # Decodifica de Base64 a binario

    # Guardar el archivo en la base de datos
    if file_type == 'xml':
        cfdi.xml_file.save(f'CFDI_{id_factura}.xml', ContentFile(file_content))
    elif file_type == 'pdf':
        cfdi.pdf_file.save(f'CFDI_{id_factura}.pdf', ContentFile(file_content))
        
    # Guardar los cambios en la factura
    cfdi.save()

def create_and_save_comp ( cfdi, file_type, id_factura ):
    response = get_cfdi_doc(file_type, id_factura)  # Llama a la función que obtiene el documento

    if response.status_code != 200:
        raise Exception(f"No se pudo descargar el {file_type.upper()}.")

    # Decodificar el JSON de la respuesta
    response_json = response.json()

    # Verifica que el campo 'Content' esté presente
    if 'Content' not in response_json:
        raise Exception("La respuesta no contiene el contenido esperado.")

    # Extraer y decodificar el contenido Base64
    file_base64 = response_json['Content']
    file_content = base64.b64decode(file_base64)  # Decodifica de Base64 a binario

    # Guardar el archivo en la base de datos
    if file_type == 'xml':
        cfdi.xml_file.save(f'CFDI_{id_factura}.xml', ContentFile(file_content))
    elif file_type == 'pdf':
        cfdi.pdf_file.save(f'CFDI_{id_factura}.pdf', ContentFile(file_content))
        
    # Guardar los cambios en el comprobante
    cfdi.save()

# ------------------------------- #
#   PETICIONES DEL SISTEMA
# ------------------------------- #

@login_required
@transaction.atomic
def cargar_csd(request):
    # https://apisandbox.facturama.mx/guias/api-multi/csds
    if request.method == 'POST':
        form = CSDForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar en la BD
            csd = form.save(commit=False)

            # Obtener la organización seleccionada en el formulario
            # El formulario incluiría un campo para seleccionar la organización
            organizacion =request.user.organizacion

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
            url = f"{SANDBOX_URL}/api-lite/csds"
            response = requests.post(url, json=csd_data, auth=(USERNAME, PASSWORD))

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

@login_required
@transaction.atomic
def eliminar_csd(request):
    if request.method == 'POST':
        # Verificamos que la petición es de tipo AJAX
        if request.headers.get('Content-Type') == 'application/json':
            try:
                organizacion = request.user.organizacion
                # Eliminar los CSD asociados a la organización del usuario
                CSD.objects.filter(organizacion=organizacion).delete()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
@transaction.atomic
def crear_factura(request, id_personalizado):
    
    # Obtener la orden de trabajo
    orden = OrdenTrabajo.objects.get(id_personalizado=id_personalizado)
    cliente = orden.cotizacion.persona
    emisor = orden.cotizacion.usuario
    conceptos = OrdenTrabajoConcepto.objects.filter(orden_de_trabajo=id_personalizado)

    if request.method == 'POST':
        
        encabezado_form = FacturaEncabezadoForm(request.POST, initial={'OrderNumber': orden.id_personalizado})
        pie_form = FacturaPieForm(request.POST, initial={'direccion': orden.direccion})
        totales_form = FacturaTotalesForm(request.POST)
        
        if encabezado_form.is_valid() and pie_form.is_valid() and totales_form.is_valid():

            # Obteniendo datos de formularios
            datos_e = encabezado_form.cleaned_data
            datos_p = pie_form.cleaned_data
            datos_t = totales_form.cleaned_data
            
            direccion = datos_p['direccion']
            subtotal = datos_t['subtotal']
            iva = datos_t['iva']
            total = datos_t['total']

            # Iteramos sobre los conceptos
            conceptos_data = []
            for i in range(1, len(request.POST) + 1):
                codigo_servicio = request.POST.get(f'concepto.concepto.servicio.codigo_{i}')
                nombre_servicio = request.POST.get(f'nombre_servicio_{i}')
                metodo = request.POST.get(f'metodo_{i}')
                cantidad_servicios = request.POST.get(f'cantidad_servicios_{i}')
                precio = request.POST.get(f'precio_{i}')
                importe = request.POST.get(f'importe_{i}')

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

            print(aware_datetime.isoformat())
            cfdi_data = {
                "NameId": "1",
                "Currency": datos_e['tipo_moneda'],
                "Folio": get_new_cfdi_id(),
                "Serie": "FAC",
                "Date": aware_datetime.isoformat(),  # Fecha actual en formato ISO 8601
                "CfdiType": "I",
                "LogoUrl": "",# ( string ) Url del logo, ej. https://dominio.com/mi-logo.png
                "PaymentForm": datos_e['forma_pago'],
                "PaymentMethod": datos_e['metodo_pago'],
                "ExpeditionPlace": emisor.organizacion.direccion.codigo,
                "Observations": datos_p['comentarios'],
                "OrderNumber": datos_e['OrderNumber'],
                "Issuer": {  # ( TaxEntityInfoViewModel ) Nodo que contiene el detalle del emisor.
                    "Rfc": get_emisor(request),
                    "Name": emisor.organizacion.nombre,
                    "FiscalRegime": emisor.organizacion.regimen_fiscal
                },
                "Receiver": {  # Receiver ( ReceiverV4BindingModel ) Cliente a quien se emitirá el CFDi, Atributo Requerido
                    "Rfc": request.POST.get('id_cliente_rfc'),
                    "Name": request.POST.get('id_cliente_nombre'),
                    "CfdiUse": datos_e['uso_cfdi'],
                    "FiscalRegime": request.POST.get('id_cliente_reg'),
                    "TaxZipCode": cliente.empresa.direccion.codigo,
                    "Address": {
                        "Street": cliente.empresa.direccion.calle,
                        "Neighborhood": cliente.empresa.direccion.colonia,
                        "ZipCode": cliente.empresa.direccion.codigo,
                        "Municipality": cliente.empresa.direccion.ciudad,
                        "State": cliente.empresa.direccion.estado,
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
                                "Total": float(concepto['importe']) * datos_t['tasa_iva'],
                                "Name": "IVA",
                                "Base": float(concepto['importe']),
                                "Rate": datos_t['tasa_iva'],
                                "IsRetention": False
                            }
                        ],
                        "Total": round(float(concepto['importe']) * 1.16, 2)
                    }
                    for concepto in conceptos_data
                ]
            }
            
            
            
            print(get_new_cfdi_id())
            response = crear_cfdi_api(cfdi_data)

            if response.status_code == 201:
                
                response_data = response.json()
                print(json.dumps(response_data, indent=4))
                print(request , messages)
                cfdi_id = response_data.get("Id")
                messages.success(request, 'CFDI timbrado correctamente.')
                nueva_factura = Factura(
                    # Aquí debes agregar los campos necesarios para la factura
                    id=response_data.get("Folio"),
                    cfdi_id=response_data.get("Id"),
                    cfdi_type = response_data.get("CfdiType"),
                    Type = response_data.get("Type"),
                    orden=orden,
                    OrderNumber=datos_e['OrderNumber'],
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
                    estado=response_data.get("Status"),
                    OriginalString=response_data.get("OriginalString"),
                    CfdiSign=response_data.get("Complement", {}).get("TaxStamp", {}).get("CfdiSign"),
                    SatSign=response_data.get("Complement", {}).get("TaxStamp", {}).get("SatSign"),
                )
                nueva_factura.save() 
                return redirect('factura_detalle',  cfdi_id )
            else:
                # Si ocurre un error, mostrar un mensaje detallado
                error_code = response.status_code
                error_message = response.json().get("message", "Ocurrió un error inesperado.")
                full_error_message = f"Error al cargar CSD. Código: {error_code}. Mensaje: {error_message}. Detalles: {response.text}"
                messages.error(request, full_error_message)
        return redirect('home')
    
    encabezado_form = FacturaEncabezadoForm(initial={'OrderNumber': orden.id_personalizado, 'tipo_moneda': orden.cotizacion.metodo_pago})
    pie_form = FacturaPieForm(initial={'direccion': orden.direccion,'comentarios': orden.cotizacion.notas})
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
@transaction.atomic
def download_factura(request, id_factura, file_type):
    try:
        # Obtener la factura desde la base de datos
        cfdi = get_object_or_404(Factura, cfdi_id=id_factura)

        # Verificar si el archivo ya existe en la base de datos
        if (file_type == 'xml' and cfdi.xml_file) or (file_type == 'pdf' and cfdi.pdf_file):
            # Si ya existe, retornamos el archivo guardado
            file_field = cfdi.xml_file if file_type == 'xml' else cfdi.pdf_file
            response = FileResponse(file_field.open(), content_type=f'application/{file_type}')
            response['Content-Disposition'] = f'attachment; filename=CFDI_{id_factura}.{file_type}'
            return response
        
        # Descarga XML o PDF basado en el tipo
        response = get_cfdi_doc(file_type, id_factura)  # Cambia a solo una llamada

        if response.status_code != 200:
            raise Http404(f"No se pudo descargar el {file_type.upper()}.")
        
        # Decodificar el JSON de la respuesta
        response_json = response.json()
        
        # Verifica que el campo 'Content' esté presente
        if 'Content' not in response_json:
            raise Http404("La respuesta no contiene el contenido esperado.")

        # Extraer y decodificar el contenido Base64
        file_base64 = response_json['Content']
        file_content = base64.b64decode(file_base64)  # Decodifica de Base64 a binario
        
        # Guardar el archivo en la base de datos
        if file_type == 'xml':
            cfdi.xml_file.save(f'CFDI_{id_factura}.xml', ContentFile(file_content))
        elif file_type == 'pdf':
            cfdi.pdf_file.save(f'CFDI_{id_factura}.pdf', ContentFile(file_content))
            
        # Guardar los cambios en la factura
        cfdi.save()
        
        # Determina el tipo de archivo (PDF o XML)
        content_type = 'application/xml' if file_type == 'xml' else 'application/pdf'
        filename = f'CFDI_{id_factura}.{file_type}'

        # Crear la respuesta HTTP con el archivo
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    except Exception as e:
        raise Http404(f"Error al descargar el documento: {str(e)}")

@login_required
@transaction.atomic
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
     
@login_required 
@transaction.atomic
def comprobante_factura(request, cfdi_id):
    factura = get_object_or_404(Factura, cfdi_id=cfdi_id)  # Mover esta línea al inicio

    if request.method == 'POST':
        
        form = ComprobantePagoForm(request.POST)
        
        if form.is_valid():
            
            # Obtener datos del formulario
            date = request.POST.get('Date')
            PaymentForm = request.POST.get('PaymentForm')
            Amount = request.POST.get('Amount')
            OperationNumber = request.POST.get('OperationNumber')
            ForeignAccountNamePayer = request.POST.get('ForeignAccountNamePayer')
            PayerAccount = request.POST.get('PayerAccount')  # Corrección aquí
            RfcReceiverBeneficiaryAccount = request.POST.get('RfcReceiverBeneficiaryAccount')
            BeneficiaryAccount = request.POST.get('BeneficiaryAccount')
            
            organizacion = factura.emisor
            csd = get_object_or_404(CSD, organizacion = organizacion)
            Rfc = csd.rfc
            
            # Conversión de valores Decimal a cadena
            def decimal_to_str(value):
                return str(value) if isinstance(value, Decimal) else value
            
            cfdi_api = buscar_cfdi_return(cfdi_id)
            
            idd = get_new_cfdi_comp_id()
            
            #Aquí debes construir el JSON para la API de Facturama
            complemento_pago = {
                "NameId": "14", # Numero de referencia que  indica tipo de factura comprobante de pago
                "Folio": idd,  # Folio de la factura o comprobante
                "Serie": "COP",
                "CfdiType": "P",
                "OrderNumber": str(factura.orden.id_personalizado),  # ID de la orden
                "ExpeditionPlace": factura.ExpeditionPlace,
                "Date": date,
                "Observations": "Comprobante de pago",
                "Issuer": {
                    "Rfc": Rfc,  # El modelo Organización o Factura debe tener un RFC
                    "Name": factura.emisor.nombre,
                    "FiscalRegime": factura.emisor.regimen_fiscal
                },
                "Receiver": {
                    "Rfc": factura.cliente.empresa.rfc, 
                    "CfdiUse": "CP01",  # Ajustado a CP01 para comprobante de pago
                    "Name": factura.cliente.empresa.nombre_empresa,
                    "FiscalRegime": factura.cliente.empresa.regimen_fiscal,
                    "TaxZipCode": factura.cliente.empresa.direccion.codigo,
                },
                "Complemento": {
                    "Payments": [
                        {
                            "Date": date,
                            "PaymentForm": PaymentForm,
                            "Amount": Amount,
                            "OperationNumber": OperationNumber,
                            
                            "RfcIssuerPayerAccount": Rfc, 
                            "ForeignAccountNamePayer": ForeignAccountNamePayer, 
                            "PayerAccount": PayerAccount, 
                            "RfcReceiverBeneficiaryAccount": RfcReceiverBeneficiaryAccount, 
                            "BeneficiaryAccount": BeneficiaryAccount,
                            "RelatedDocuments": [
                                {
                                    "TaxObject": "01",  # Ajustado a 01 para no manerjar impuestos aún :(
                                    "Uuid": cfdi_api.get("uuid"),  # Sacado de GET {{SANDBOX_URL}}/cfdi?type=issuedLite&rfcIssuer=EKU9003173C9
                                    "PartialityNumber": "1",
                                    "Folio": str(factura.id),  # El folio es el id
                                    "Currency": factura.tipo_moneda,
                                    "PaymentMethod": "PUE",  # Ajustar a un método de pago válido
                                    "PreviousBalanceAmount": decimal_to_str(factura.total),
                                    "AmountPaid": Amount,
                                    "ImpSaldoInsoluto": "0"
                                }
                            ]
                        }
                    ]
                }
            }
            # Condicionales para PaymentForm
            if complemento_pago['Complemento']['Payments'][0]['PaymentForm'] in ['01', '02']:
                # Si es 01, eliminamos las claves no necesarias
                complemento_pago['Complemento']['Payments'][0].pop('RfcIssuerPayerAccount', None)
                complemento_pago['Complemento']['Payments'][0].pop('PayerAccount', None)
                complemento_pago['Complemento']['Payments'][0].pop('RfcReceiverBeneficiaryAccount', None)
                complemento_pago['Complemento']['Payments'][0].pop('BeneficiaryAccount', None)
            else:
                # Agregar campos relevantes si PaymentForm no es 01
                complemento_pago['Complemento']['Payments'][0]['RfcIssuerPayerAccount'] = Rfc
                complemento_pago['Complemento']['Payments'][0]['PayerAccount'] = PayerAccount
                complemento_pago['Complemento']['Payments'][0]['RfcReceiverBeneficiaryAccount'] = RfcReceiverBeneficiaryAccount
                complemento_pago['Complemento']['Payments'][0]['BeneficiaryAccount'] = BeneficiaryAccount

            complemento_pago['Complemento']['Payments'][0]['RelatedDocuments'] = [
                {
                    "TaxObject": "01",
                    "Uuid": cfdi_api.get("uuid"),
                    "PartialityNumber": "1",
                    "Folio": str(factura.id),
                    "Currency": factura.tipo_moneda,
                    "PaymentMethod": "PUE",
                    "PreviousBalanceAmount": decimal_to_str(factura.total),
                    "AmountPaid": Amount,
                    "ImpSaldoInsoluto": "0"
                }
            ]
            
            # Aquí puedes añadir más lógica para procesar los datos
            response = crear_cfdi_api(complemento_pago)
            
            if response.status_code in [200, 201]:
                
                response_data = response.json()
                print(response_data)  # Verifica qué está llegando en la respuesta
                
                # # Guarda factrura en la BD
                comprobante = Comprobante.objects.create(
                    folio = idd,
                    factura = factura,
                    cfdi_id = response_data.get("Id"),
                    fecha_pago = date,
                    monto_pagado = Amount,
                    metodo_pago = PaymentForm,
                )
                comprobante.save()
                
                factura.estado = 'paid'
                
                messages.success(request, 'CFDI Comrpobante de pago timbrado correctamente.')
            if response.status_code == 400:
                # Error de validación de la API
                response_data = response.json()
                return JsonResponse({'success': False, 'message': 'Error de validación en la API. Verifica los datos.', 'response_data': response_data}, status=400)  # Método no permitido
            elif response.status_code == 500:
                # Error interno de la API
                response_data = response.json()
                return JsonResponse({'success': False, 'message': 'Error en el servidor. Inténtalo de nuevo más tarde.', 'response_data': response_data}, status=400)  # Método no permitido
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  # En caso de que el formulario no sea válido
    else:
        form = ComprobantePagoForm(initial={
            'Amount': factura.total,
            'OperationNumber': factura.id,
            'ForeignAccountNamePayer': factura.cliente.empresa.nombre_empresa,
            'RfcReceiverBeneficiaryAccount': factura.cliente.empresa.rfc
        })
    # Para el caso GET, simplemente renderiza la plantilla con el formulario

    return redirect('factura_detalle', cfdi_id=factura.cfdi_id)

@login_required
@transaction.atomic
def CF(request):
    form = FacturaForm()
    cotizaciones = Cotizacion.objects.all()
    context = {
        'form': form,
        'cotizaciones': cotizaciones,
    }
    return render(request, "cotizaciones.html", context)

@login_required
@transaction.atomic
def download_comprobante(request, id_factura, file_type):
    try:
        # Obtener la factura desde la base de datos
        cfdi = get_object_or_404(Comprobante, cfdi_id=id_factura)

        # Verificar si el archivo ya existe en la base de datos
        if (file_type == 'xml' and cfdi.xml_file) or (file_type == 'pdf' and cfdi.pdf_file):
            # Si ya existe, retornamos el archivo guardado
            file_field = cfdi.xml_file if file_type == 'xml' else cfdi.pdf_file
            response = FileResponse(file_field.open(), content_type=f'application/{file_type}')
            response['Content-Disposition'] = f'attachment; filename=CFDI_{id_factura}.{file_type}'
            return response
        
        # Descarga XML o PDF basado en el tipo
        response = get_cfdi_doc(file_type, id_factura)  # Cambia a solo una llamada

        if response.status_code != 200:
            raise Http404(f"No se pudo descargar el {file_type.upper()}.")
        
        # Decodificar el JSON de la respuesta
        response_json = response.json()
        
        # Verifica que el campo 'Content' esté presente
        if 'Content' not in response_json:
            raise Http404("La respuesta no contiene el contenido esperado.")

        # Extraer y decodificar el contenido Base64
        file_base64 = response_json['Content']
        file_content = base64.b64decode(file_base64)  # Decodifica de Base64 a binario
        
        # Guardar el archivo en la base de datos
        if file_type == 'xml':
            cfdi.xml_file.save(f'CFDI_{id_factura}.xml', ContentFile(file_content))
        elif file_type == 'pdf':
            cfdi.pdf_file.save(f'CFDI_{id_factura}.pdf', ContentFile(file_content))
            
        # Guardar los cambios en la factura
        cfdi.save()
        
        # Determina el tipo de archivo (PDF o XML)
        content_type = 'application/xml' if file_type == 'xml' else 'application/pdf'
        filename = f'CFDI_{id_factura}.{file_type}'

        # Crear la respuesta HTTP con el archivo
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    except Exception as e:
        raise Http404(f"Error al descargar el documento: {str(e)}")

@login_required
@transaction.atomic
def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)  # Crear una instancia del formulario con los datos del POST
        if form.is_valid():  # Verificar que el formulario sea válido
            # Obtener los datos del formulario
            cfdi_id = form.cleaned_data['cfdi_id']  # Obtener el cfdi_id
            recipient_emails = form.cleaned_data['emails'].split(',')
            bcc_emails = form.cleaned_data['bcc_emails'].split(',')
            need_factura = form.cleaned_data['need_factura']
            need_comprobante = form.cleaned_data['need_comprobante']
            mensaje = form.cleaned_data['mensaje']  # Obtener el mensaje

            # Buscar la factura usando el cfdi_id
            factura = get_object_or_404(Factura, cfdi_id = cfdi_id)   # Cambia 'id' por el campo correcto si es necesario
            
            # Verificar y crear los archivos si no existen
            if need_factura:
                if not factura.xml_file or not os.path.exists(factura.xml_file.path):
                    create_and_save_fac(factura, 'xml', cfdi_id)

                if not factura.pdf_file or not os.path.exists(factura.pdf_file.path):
                    create_and_save_fac(factura, 'pdf', cfdi_id)
                    
            # Verificar y crear los archivos de los comprobantes si se necesitan
            if need_comprobante:
                comprobantes = factura.comprobantes.all()  # Obtener todos los comprobantes
                for comprobante in comprobantes:
                    if not comprobante.xml_file or not os.path.exists(comprobante.xml_file.path):
                        create_and_save_comp(comprobante, 'xml', comprobante.cfdi_id)  # Cambia cfdi_id si es necesario

                    if not comprobante.pdf_file or not os.path.exists(comprobante.pdf_file.path):
                        create_and_save_comp(comprobante, 'pdf', comprobante.cfdi_id)  # Cambia cfdi_id si es necesario

            # Configuración del correo
            email = EmailMessage(
                subject='Documentos adjuntos',
                body=mensaje,  # Mensaje del usuario
                from_email=EMAIL_HOST_USER,  # Cambia esto por tu correo
                to=[email.strip() for email in recipient_emails if email.strip()],  # Limpiar espacios en blanco y eliminar correos vacíos
                bcc=[bcc_email.strip() for bcc_email in bcc_emails if bcc_email.strip()]  # CCO
            )

            # Adjuntar documentos si se solicitan
            if need_factura:
                email.attach_file(factura.xml_file.path)
                email.attach_file(factura.pdf_file.path)

            if need_comprobante:
                # Obtener todos los comprobantes asociados a la factura
                comprobantes = factura.comprobantes.all()  # Obtener todos los comprobantes
                for comprobante in comprobantes:
                    email.attach_file(comprobante.xml_file.path)  # Adjuntar archivo XML
                    email.attach_file(comprobante.pdf_file.path)  # Adjuntar archivo PDF

            # Enviar el correo
            email.send()
            messages.success(request, "Correo enviado con éxito")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        return JsonResponse({'success': False, 'errors': form.errors})  # En caso de que el formulario no sea válido

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)  # Método no permitido

# ------------------------------- #
#   PETICIONES A LA API FACTURAMA
# ------------------------------- #

def cfdis_all(emisor_rfc):
    # https://apisandbox.facturama.mx/api-lite/cfdis?status=all&issued=EKU9003173C9
    url = f"{SANDBOX_URL}/api-lite/cfdis?status=all&issued={emisor_rfc}"
    response = requests.get(url,auth = (USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()

def crear_cfdi_api( data):
    
    url = f"{SANDBOX_URL}/api-lite/3/cfdis"
    response = requests.post(url, json=data, auth=(USERNAME, PASSWORD))
    return response # Puedes devolver la respuesta en JSON si lo necesitas
 
def get_cfdi_doc(doc, id_factura):
    
    url = f"{SANDBOX_URL}/cfdi/{doc}/issuedLite/{id_factura}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    return response
 
def cancelar_factura_api(factura_id, motive, uuid_replacement):
    url = f"{SANDBOX_URL}/api-lite/cfdis/{factura_id}?motive={motive}&uuidReplacement={uuid_replacement}"
    
    # Realiza la llamada a la API (usa el método que necesites, por ejemplo POST)
    try:
        # Solicitud al API de Facturama
        response = requests.delete(url, auth=(USERNAME, PASSWORD))
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

def search_cfdi_return(id):
    
    url = f"{SANDBOX_URL}/api-lite/cfdis/{id}"   
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    return response
