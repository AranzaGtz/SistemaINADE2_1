# VISTA PARA AUTENTICAR USUARIO
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.models import CustomUser, Organizacion

def login_view(request):
    context = {}
    
    if request.user.is_authenticated:
        return redirect("dashboard")  # Redirigir sin pasar organizacion

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Verificando si el usuario es trabajador o tiene permiso staff
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso!')
                return redirect("dashboard")  # Redirigir sin pasar organizacion
            else:
                context['error'] = "No tienes permisos para acceder"
                return render(request, "accounts/autenticacion/login.html", context)
        else:
            context['error'] = "Credenciales inválidas"
            return render(request, "accounts/autenticacion/login.html", context)

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
            return render(request, "accounts/otros/dashboard_coordinator.html")

        elif rol == "muestras":
            # Interfaz para el usuario de muestras
            print("Usuario es de Muestras")
            return render(request, "accounts/otros/dashboard_samples.html")

        elif rol == "informes":
            # Interfaz para el usuario de informes
            print("Usuario es de Informes")
            return render(request, "accounts/otros/dashboard_reports.html")

        elif rol == "calidad":
            # Interfaz para el usuario de calidad
            print("Usuario es de Calidad")
            return render(request, "accounts/otros/dashboard_quality.html")

        else:

            return render(request, "accounts/otros/dashboard_default.html")

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

# VISTA PARA CAMBIAR CONTRASEÑA
def recuperacion_pssw(request):
    return render(request, "accounts/autenticacion/recuperacion_pssw.html")

#vista personalizada CustomPasswordResetView
class CustomPasswordResetView(FormView):
    template_name = 'accounts/autenticacion/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        form.save(
            request=self.request,
            use_https=self.request.is_secure(),
            email_template_name='accounts/autenticacion/password_reset_email.html'
        )
        return super().form_valid(form)
