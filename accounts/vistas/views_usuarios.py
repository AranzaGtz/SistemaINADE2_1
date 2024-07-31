# views_usuarios.py

from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser
from django.contrib import messages

# VISTA PARA DIRIGIR A INTERFAZ DE USUARIO
def usuario_list(request):
    # Notificación
    notificaciones = request.user.notificacion_set.all()
    notificaciones_no_leidas = notificaciones.filter(leido=False).count()
    
    Lista_usuarios = CustomUser.objects.all()
    form = CustomUserCreationForm()
    context={
        'usuarios':Lista_usuarios,
        'form':form,
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
    }
    return render(request, "accounts/usuarios/usuarios.html",context)

# VISTA PARA REGISTRAR UN USUARIO
def usuario_create(request):

    if request.method == "POST":  # Se envio informacion

        form = CustomUserCreationForm(request.POST)  # se crea instancia del formulario

        if form.is_valid():  # Se verifica el formulario

            user = form.save(commit=False)

            user.is_staff = True  # Ajusta los atributos is_staff y is_superuser según el rol del usuario

            if ( user.rol == "admin"):  # Si el rol es admin, se establece is_superuser a True.
                user.is_superuser = True

            user.save()  # Guarda el usuario en la base de datos.
            
            messages.success(request, 'El usuario se ha registrado!.')
            
            return redirect("usuario_list")  # Redirige al usuario a login
    else:
        form = (CustomUserCreationForm())  # Si la solicitud no es POST, crea un formulario vacío.
    return render(request,'accounts/usuarios/usuarios.html',{'registro_form':form}) # Renderiza la plantilla con el formulario.

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


