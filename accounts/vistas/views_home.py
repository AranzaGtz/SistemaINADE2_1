# VISTA PARA DIRIGIR A INTERFAZ DE CLIENTES
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Notificacion

@login_required
def home(request):
    # Obtener todas las notificaciones del usuario
    notificaciones = request.user.notificacion_set.all()
    
    # Contar las notificaciones no leídas
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
    # Renderizar la plantilla con los datos
    return render(request, 'accounts/home/dashboard_admin_home.html', {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas
    })