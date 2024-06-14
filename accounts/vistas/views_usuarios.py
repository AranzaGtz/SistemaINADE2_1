from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser
from django.contrib import messages

# VISTA PARA DIRIGIR A INTERFAZ DE USUARIO
def usuario_list(request):
    Lista_usuarios = CustomUser.objects.all()
    form = CustomUserCreationForm()
    return render(request, "accounts/usuarios/dashboard_admin.html",{"usuarios": Lista_usuarios,'form':form})

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
            
            messages.success(request, 'Usuario registrado exitosamente!.')
            
            return redirect("usuario_list")  # Redirige al usuario a login
    else:
        form = (CustomUserCreationForm())  # Si la solicitud no es POST, crea un formulario vacío.
    return render(request,'accounts/usuarios/dashboard_admin.html',{'registro_form':form}) # Renderiza la plantilla con el formulario.

# VISTA PARA BORRAR USUARIO
def usuario_delete(request, username):
    usuario = CustomUser.objects.get(username = username)
    usuario.delete()
    messages.success(request, '¡Usuario eliminado exitosamente!.')
    return redirect('usuario_list')

# VISTA PARA IR EDITANDO USUARIO
def usuario_update(request,username):
    usuario = get_object_or_404(CustomUser, username = username)
    form = CustomUserChangeForm(instance=usuario)
    usuarios = CustomUser.objects.all()
    return render(request, "accounts/usuarios/dashboard_admin.html", {"usuario":usuario,"usuarios": usuarios, "form":form, "edit": True})
 
# VISTA PARA EDITAR USUARIO
def usuario_update2(request, username):
    usuario = get_object_or_404(CustomUser, username = username)
    if request.method == "POST":
        form  = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario actualizado exitosamente!.')
            return redirect("usuario_list")
    else: 
        form = CustomUserChangeForm(instance=usuario)
    return redirect(request, "usuario_list", {"usuario": usuario,"form": form,"edit":True})

