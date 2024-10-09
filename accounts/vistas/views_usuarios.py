# views_usuarios.py

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json

# VISTA PARA ACLARACIÓN DE ERRORES EN FORMULARIO DE CREACION DE USUARIOS
def verificar_usuario(request):
    username = request.GET.get('username', '')
    existe = CustomUser.objects.filter(username=username).exists()
    return JsonResponse({'exists': existe})

ROL_DESCRIPCION = {
    'admin': 'Acceso completo al sistema. Puede gestionar usuarios, cotizaciones y administrar todas las áreas.',
    'coordinador': 'Coordina las actividades del equipo y supervisa los procesos en las distintas áreas.',
    'muestras': 'Gestiona la recolección y análisis de muestras.',
    'informes': 'Encargado de la generación y revisión de informes.',
    'laboratorio': 'Realiza análisis y pruebas en el laboratorio.',
    'calidad': 'Asegura la calidad y cumplimiento de los estándares en los procesos.'
}

# VISTA PARA DIRIGIR A INTERFAZ DE USUARIO
@login_required
def usuario_list(request):
    
    # Obtener el filtro de rol de la solicitud GET, si existe
    rol = request.GET.get('rol', 'todos')

    if rol == 'todos':
        Lista_usuarios = CustomUser.objects.all()
    else:
        Lista_usuarios = CustomUser.objects.filter(rol=rol)

    # Definir descripciones de roles
    ROL_DESCRIPCION = {
        'admin': 'Administrador: Tiene acceso completo a todas las funcionalidades del sistema.',
        'coordinador': 'Coordinador: Puede gestionar proyectos y coordinar equipos.',
        'muestras': 'Muestras: Se encarga de la recolección y manejo de muestras.',
        'informes': 'Informes: Responsable de la generación y revisión de informes.',
        'laboratorio': 'Laboratorio: Gestiona las operaciones del laboratorio y pruebas.',
        'calidad': 'Calidad: Supervisa y asegura la calidad de todos los procesos.',
    }

    form = CustomUserCreationForm()
    context = {
        'usuarios': Lista_usuarios,
        'form': form,
        'rol_seleccionado': rol,
        'rol_descriptions': json.dumps(ROL_DESCRIPCION),  # Enviar descripciones al template
    }
    return render(request, "accounts/usuarios/usuarios.html", context)

# VISTA PARA REGISTRAR UN USUARIO
def usuario_create(request):
    form = CustomUserCreationForm(initial={'rol':'muestras'} )
    if request.method == "POST":  # Se envió información
        form = CustomUserCreationForm(request.POST, initial={'rol':'muestras'})  # Se crea instancia del formulario

        if form.is_valid():  # Se verifica el formulario
            user = form.save(commit=False)
            user.is_staff = True  # Ajusta los atributos is_staff y is_superuser según el rol del usuario

             # Establece el rol directamente a "muestreador"
            user.rol = "muestras"

            # Intenta asignar la organización del usuario logueado
            user.organizacion = getattr(request.user, 'organizacion', None)

            # Si no hay una organización asignada, maneja el error
            if not user.organizacion:
                messages.error(request, 'No se ha podido asignar una organización. Verifica que el usuario actual tenga una organización asociada.')
                return render(request, 'accounts/usuarios/usuarios.html', {'registro_form': form})

            try:
                user.save()  # Guarda el usuario en la base de datos
                messages.success(request, 'El usuario se ha registrado correctamente.')
                return redirect("usuario_list")  # Redirige al usuario a la lista de usuarios
            except Exception as e:
                messages.error(request, f'Error al guardar el usuario: {e}')
                return render(request, 'accounts/usuarios/usuarios.html', {'registro_form': form})

    else:
        form = CustomUserCreationForm(initial={'rol':'muestras'})  # Si la solicitud no es POST, crea un formulario vacío.

    return render(request, 'accounts/usuarios/usuarios.html', {'registro_form': form})  # Renderiza la plantilla con el formulario.

# VISTA PARA IR EDITANDO USUARIO
def usuario_update(request,username):
    # Obtiene usuario por su username o muestra un 404 si no se encuentra
    usuario = get_object_or_404(CustomUser, username = username)
    
    if request.method == 'POST':
        # Crea un formulario con los datos enviados y la instancia de usuario
        usuario_form = CustomUserChangeForm(request.POST, instance=usuario)
        if usuario_form.is_valid():
            # Guarda la usuario
            usuario_form.save()
            # Muestra un mensaje de éxito y redirige a la lista de usuarios
            messages.success(request, 'Usuario actualizado con éxito!')
            return redirect('usuario_list')
    else:

        # Si no es un POST, inicializa el formulario con los datos actuales del usuario
        usuario_form = CustomUserChangeForm(instance=usuario)

    # Contexto que se pasa a la plantilla
    context = {
        'persona_form': usuario_form,
        'persona': usuario,
    }
    
    # Renderiza la plantilla de edición de usuario con el contexto
    return render(request, 'accounts/usuarios/editar_usuario.html', context)
 
# VISTA PARA ELIMINAR usuario
def usuario_delete(request, id):
    usuario = get_object_or_404(CustomUser, id=id)
    usuario.delete()
    messages.success(request, 'Usuario Eliminado!.')
    # Redirigir a la lista de cotizaciones después de la eliminación
    return redirect('usuario_list')


