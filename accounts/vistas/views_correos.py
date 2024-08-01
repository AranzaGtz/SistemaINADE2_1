from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import EmailMessage
from accounts.models import Cotizacion, Notificacion, CustomUser, Persona
from accounts.forms import OrdenPedidoForm
from django.contrib import messages
from django.urls import reverse

#   VISTA PARA ENVIAR COTIZACIÓN
def enviar_cotizacion(request, pk, destinatarios):
    # Obtiene la cotización correspondiente al id proporcionado o devuelve un error 404 si no se encuentra
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    
    # Construir la URL de confirmación
    form_url = request.build_absolute_uri(reverse('formulario_descarga_subida', args=[cotizacion.id,request.user.username]))

    # Prepara el asunto y mensaje del correo electrónico
    subject = f'Cotización {cotizacion.id_personalizado}'
    message = f'''
    Estimado/a cliente,
    
        Adjunto a este correo encontrará la cotización solicitada con el ID {cotizacion.id_personalizado}.
        Para descargar la cotización y subir su orden de trabajo, haga clic en el siguiente enlace: {form_url}
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
    
     # Adjuntar el PDF guardado en la base de datos
    if cotizacion.cotizacion_pdf:
        email.attach_file(cotizacion.cotizacion_pdf.path)

    # Enviar el correo electrónico
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
    correos_adicionales = cotizacion.correos_adicionales.split(",") if cotizacion.correos_adicionales else []

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

#   FORMULARIO PARA ORDEN DE PEDIDOS DE LOS USUARIO
def formulario_descarga_subida(request, pk, usuario):
    cotizacion = get_object_or_404(Cotizacion, id=pk)
    # Intentar obtener el usuario
    try:
        usuario_obj = CustomUser.objects.get(username=usuario)
    except CustomUser.DoesNotExist:
        messages.error(request, 'El usuario no existe. Verifique el enlace proporcionado.')
        return redirect('login')  # Redirigir al inicio de sesión o a una página adecuada

    if request.method == 'POST':
        form = OrdenPedidoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo']
            cotizacion.orden_pedido_pdf.save(archivo.name, archivo)  # Guardar el archivo correctamente
            cotizacion.save()

            # Crear la notificación con el usuario objeto
            Notificacion.objects.create(
                usuario=usuario_obj,  # Utiliza el objeto de usuario
                tipo='orden_trabajo_subida',
                mensaje=f'Se ha subido la orden de trabajo para la cotización {cotizacion.id}',
                enlace=reverse('cotizacion_detalle', args=[cotizacion.id])
            )
            messages.success(request, 'Orden de trabajo subida exitosamente.')
            return redirect('confirmacion_recepcion')
    else:
        form = OrdenPedidoForm()
    return render(request, 'accounts/correos/formulario_descarga_subida.html', {'cotizacion': cotizacion, 'form': form})    
