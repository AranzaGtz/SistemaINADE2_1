# VISTA PARA AUTENTICAR USUARIO
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.models import CustomUser

def login_view(request):
    
    context = {}
    
    if request.user.is_authenticated:
        return redirect("dashboard") # AQUI QUIERO ACTUALIZA PAGUINA

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if (
                user.is_staff
            ):  # Verificando si el usuaro es trabajador o tiene permiso staff

                login(request, user)
                messages.success(request, 'Inicio de sesion exitosa.!')
                return redirect("dashboard")
            else:
                
                context['error'] = "No tienes permisos para acceder"
                
                return render(
                    request,
                    "accounts/autenticacion/login.html",context,
                )
        else:
            
            context['error'] = "Credenciales invalidas"
            
            return render(
                request, "accounts/autenticacion/login.html", context
            )
            # Redirige al usuario a alguna página después de iniciar sesión correctamente
            # Renderizar la plantilla con el contexto
    response = render(request, "accounts/autenticacion/login.html", context)
    
    
    return render(request, "accounts/autenticacion/login.html", context)

# VISTA PARA SALIR DE SESION
def logout_view(request):
    logout(request)
    return redirect(
        "login"
    )  # Cambia 'login' por la URL a la que quieres redirigir tras el cierre de sesión

# VISTA PARA REDIRIGIR A USUARIO A LA INTERFAZ DE SU ROL
def dashboard(request):
    # Aquí puedes poner la lógica para determinar qué interfaz mostrar según el rol del usuario
    if request.user.is_authenticated:

        rol = request.user.rol

        if rol == "admin":
            # Interfaz para el usuario administrador
            print("Usuario es superuser")
            return redirect('home')

        elif rol == "coordinador":
            # Interfaz para el coordinador
            print("Usuario es Coordinador")
            return render(request, "accounts/dashboard_coordinator.html")

        elif rol == "muestras":
            # Interfaz para el usuario de muestras
            print("Usuario es de Muestras")
            return render(request, "accounts/dashboard_samples.html")

        elif rol == "informes":
            # Interfaz para el usuario de informes
            print("Usuario es de Informes")
            return render(request, "accounts/dashboard_reports.html")

        elif rol == "calidad":
            # Interfaz para el usuario de calidad
            print("Usuario es de Calidad")
            return render(request, "accounts/dashboard_quality.html")

        else:

            return render(request, "accounts/dashboard_default.html")

    # Redirigir a la página de inicio de sesión si el usuario no está autenticado
    print("Usuario no autenticado")
    return redirect(
        "login"
    )  # Ajusta 'login' según la URL de tu vista de inicio de sesión

# VISTA PARA MOSTRAR USUARIOS
def mostrar_CustomUser(request):
    custom_Users = CustomUser.objects.all()
    return render(
        request, "accounts/usuarios/dashboard_admin.html", {"custom_Users": custom_Users}
    )

