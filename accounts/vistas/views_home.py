# VISTA PARA DIRIGIR A INTERFAZ DE CLIENTES
from django.shortcuts import render


def home(request):
    return render(request,"accounts/home/dashboard_admin_home.html")
