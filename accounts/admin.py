from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Concepto, Cotizacion, CustomUser, Direccion, Empresa, Formato, InformacionContacto, Metodo, OrdenTrabajo, Organizacion, Persona, Prospecto, Servicio, Titulo

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'rol')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'rol')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'celular', 'rol')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'celular', 'rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

# Registrando todos los modelos en el admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Concepto)
admin.site.register(Cotizacion)
admin.site.register(Direccion)
admin.site.register(Empresa)
admin.site.register(InformacionContacto)
admin.site.register(Metodo)
admin.site.register(Persona)
admin.site.register(Prospecto)
admin.site.register(Servicio)
admin.site.register(Titulo)
admin.site.register(Organizacion)
admin.site.register(Formato)
admin.site.register(OrdenTrabajo)