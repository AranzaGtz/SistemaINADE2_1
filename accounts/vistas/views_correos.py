from datetime import datetime
from django import forms
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import EmailMessage
from SistemaINADE2 import settings
from accounts.models import Cotizacion, Concepto, Notificacion, Organizacion, Formato, CustomUser, Persona
from accounts.forms import ConceptoForm, CotizacionForm, ConceptoFormSet, FormularioSolicitudCotizacion
from django.contrib import messages
from django.db import IntegrityError
from django.template.loader import render_to_string
from weasyprint import HTML  # type: ignore # Asegúrate de tener weasyprint instalado
from django.urls import reverse
from accounts.helpers import get_formato_default, get_unica_organizacion

#   VISTA PARA ENVIAR CORREO DE TEXTO
def enviar_correo(request):
    if request.method == 'POST':
        asunto = 'Cotización creada'
        mensaje = 'La cotización ha sido creada exitosamente.'
        # Cambia esto por la dirección de correo deseada
        destinatario = ['aranza.gutierrezm.ok@gmail.com']

        send_mail(asunto, mensaje, 'proyectos.inade@icloud.com', destinatario)

        return HttpResponse('Correo enviado exitosamente.')
    return render(request, 'accounts/correos/enviar_correo.html')

#   VISTA PARA ENVIAR COTIZACIÓN
def enviar_cotizacion(request, pk, destinatarios):
    # Obtiene la cotización correspondiente al id proporcionado o devuelve un error 404 si no se encuentra
    cotizacion = get_object_or_404(Cotizacion, id=pk)

    # Obtiene todos los conceptos asociados a la cotización
    conceptos = cotizacion.conceptos.all()

    # Obtiene la organización y el formato por sus id (en este caso asumiendo que id=1 es válido)
    ogr = get_unica_organizacion()
    formato = get_formato_default(ogr)

    # Calcula el subtotal para cada concepto multiplicando la cantidad de servicios por el precio
    for concepto in conceptos:
        concepto.subtotal = concepto.cantidad_servicios * concepto.precio

    # Construye la URL absoluta del logo para incluirla en el PDF
    logo_url = request.build_absolute_uri('/static/img/logo.png')

    # Obtiene la fecha actual en el formato "YYYY/MM/DD"
    current_date = datetime.now().strftime("%Y/%m/%d")

    # Prepara el contexto con toda la información necesaria para renderizar la plantilla
    context = {
        'org': ogr,
        'org_form': formato,
        'user': request.user,
        'cotizacion': cotizacion,
        'conceptos': conceptos,
        'current_date': current_date,
        'logo_url': logo_url,
    }

    # Renderiza la plantilla HTML con el contexto proporcionado
    html_string = render_to_string('accounts/cotizaciones/cotizacion_platilla.html', context)

    # Convierte el HTML renderizado en un archivo PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    # Construir la URL de confirmación
    confirm_url = request.build_absolute_uri(reverse('confirmar_recepcion', args=[cotizacion.id]))

    form_url = request.build_absolute_uri(reverse('formulario_descarga_subida', args=[cotizacion.id]))
    
    # Prepara el asunto y mensaje del correo electrónico
    subject = f'Cotización {cotizacion.id_personalizado}'
    message = f'''
    Estimado/a cliente,

    Adjunto a este correo encontrará la cotización solicitada con el ID {cotizacion.id_personalizado}.

    Por favor, revise el documento adjunto y confirme la recepción de la cotización haciendo clic en el siguiente enlace:
    {confirm_url}

    Para descargar la cotización y subir su orden de trabajo, haga clic en el siguiente enlace:
    {form_url}

    Si tiene alguna pregunta o necesita más información, no dude en ponerse en contacto con nosotros a través de este correo.

    Agradecemos su atención y esperamos poder colaborar con usted.

    Atentamente,
    El equipo de INADE Servicios Ambientales

    ---
    Este es un correo generado automáticamente, por favor no responda a este mensaje.
    '''

    # Crea el objeto EmailMessage, adjunta el PDF y envía el correo a los destinatarios proporcionados
    email = EmailMessage(
        subject, message, 'proyectos.inade@icloud.com', destinatarios)
    email.attach(f'cotizacion_{cotizacion.id_personalizado}.pdf', pdf, 'application/pdf')
    email.send()

    messages.success(request, 'Cotización enviada por correo.')

    # Redirige al usuario a la página de detalles de la cotización
    return redirect('cotizacion_detalle', pk=cotizacion.id)

#   VISTA PARA SELECCIONAR CORREOS Y ENVIAR COTIZACIÓN
def seleccionar_correos(request, pk):
    # Obtiene la cotización correspondiente al id proporcionado o devuelve un error 404 si no se encuentra
    cotizacion = get_object_or_404(Cotizacion, id=pk)

    # Obtiene la persona (cliente) asociada a la cotización o devuelve un error 404 si no se encuentra
    cliente = get_object_or_404(Persona, id=cotizacion.persona.id)

    # Obtiene la información de contacto del cliente
    cliente_info = cliente.informacion_contacto

    # Obtiene el correo electrónico del cliente, si existe la información de contacto
    cliente_correo = cliente_info.correo_electronico if cliente_info else None

    # Obtiene el usuario actual del sistema
    usuario = get_object_or_404(CustomUser, username=request.user.username)

    # Obtiene el correo electrónico del usuario
    usuario_correo = usuario.email

    # Separa los correos adicionales de la cotización en una lista, si existen
    correos_adicionales = cotizacion.correos_adicionales.split(
        ",") if cotizacion.correos_adicionales else []

    # Si se envía una solicitud POST (por ejemplo, al enviar el formulario)
    if request.method == 'POST':
        destinatarios = []

        # Agrega el correo del cliente a la lista de destinatarios si está seleccionado en el formulario y existe el correo
        if 'cliente' in request.POST and cliente_correo:
            destinatarios.append(cliente_correo)

        # Agrega el correo del usuario a la lista de destinatarios si está seleccionado en el formulario
        if 'usuario' in request.POST:
            destinatarios.append(usuario_correo)

        # Agrega los correos adicionales seleccionados en el formulario a la lista de destinatarios
        for correo in correos_adicionales:
            if correo in request.POST:
                destinatarios.append(correo)

        # Llama a la función enviar_cotizacion para enviar la cotización a los destinatarios seleccionados
        return enviar_cotizacion(request, cotizacion.id, destinatarios)

    # Renderiza la plantilla seleccionar_correos.html con los datos necesarios
    return render(request, 'accounts/correos/seleccionar_correos.html', {
        'cotizacion': cotizacion,
        'cliente_correo': cliente_correo,
        'usuario_correo': usuario_correo,
        'correos_adicionales': correos_adicionales
    })

#   VISTA PARA RENDERIZAR FORMULARIO DE CONFIRMACIÓN
def confirmar_recepcion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    if request.method == 'POST':
        messages.success(
            request, 'Gracias por confirmar la recepción de la cotización.')
        # Aquí puedes realizar acciones adicionales como actualizar el estado de la cotización en la base de datos
        # Redirigir a la página de inicio o donde prefieras
        return redirect('confirmacion_recepcion')
    return render(request, 'accounts/correos/confirmar_recepcion.html', {'cotizacion': cotizacion})

#   VISTA DE CONFIRMACIÓN
def confirmacion_recepcion(request):
    return render(request, 'accounts/correos/confirmacion_recepcion.html')

# ---       CORREOS     ---

#   FORMULARIO PARA ORDEN DE PEDIDOS DE LOS USUARIOS
class OrdenTrabajoForm(forms.Form):
    archivo = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'archivo', 'onchange': 'actualizarNombreArchivo(this)'}),
        label=''
    )

def formulario_descarga_subida(request, pk):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo']
            # Aquí guardamos el archivo en el sistema de archivos o en la base de datos
             # Crear una notificación
            Notificacion.objects.create(
                usuario=request.user,
                tipo='orden_trabajo_subida',
                mensaje=f'Se ha subido la orden de trabajo para la cotización {cotizacion.id}',
                enlace=reverse('cotizacion_detalle', args=[cotizacion.id])
            )
            # Por simplicidad, solo mostramos un mensaje de éxito
            messages.success(request, 'Orden de trabajo subida exitosamente.')
            return redirect('confirmacion_recepcion')
    else:
        form = OrdenTrabajoForm()
    return render(request, 'accounts/correos/formulario_descarga_subida.html', {'cotizacion': cotizacion, 'form': form})
