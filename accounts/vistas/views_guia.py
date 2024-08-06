#   VISTA PARA DIRIGIR A GUIA DE OPERACIONES
from django.shortcuts import render

#    ABRIR GUIA
def guia_operaciones(request):
    return render(request, 'accounts/guia/guia_operaciones.html')

#    AGREGAR USUARIO
def guia_add_u(request):
     return render(request, 'accounts/guia/usuarios/agregar.html')

#    ELIMINAR USUARIO
