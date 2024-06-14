# VISTA PARA DIRIGIR A INTERFAZ DE CLIENTES
from django.shortcuts import render


def int_cotizaciones(request):
    # Lista_clientes = Empresa.objects.all()
    return render(request, "accounts/cotizaciones/dashboard_admin_cotizaciones.html") #,{"empresas":Lista_clientes}


