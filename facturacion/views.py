from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
import requests
from accounts.models import Cotizacion, OrdenTrabajo
from facturacion.models import Factura
from .forms import CSDForm
from django.contrib import messages
import base64

# Create your views here.
#    VISTA DE FORMULARIO DE CREACIÓN DE FACTURA
def crear_factura(request, id_personalizado):
     orden = get_object_or_404(OrdenTrabajo, id_personalizado = id_personalizado)
     context = {
          'orden': orden
     }
     return render(request,'facturacion/formulario.html',context)

#    VISTA PARA GESTIONAR EL FORMULARIO
from django.contrib.auth.decorators import login_required
# VISTA PARA GESTIONAR EL FORMULARIO

@login_required
def cargar_csd(request):
     if request.method == 'POST':
          form = CSDForm(request.POST, request.FILES)
          if form.is_valid():
               rfc = form.cleaned_data['rfc']
               certificate_path = form.cleaned_data['cer_file']
               private_key_path = form.cleaned_data['key_file']
               key_password = form.cleaned_data['password']
               

               # Leer y codificar el archivo .cer
               with open(certificate_path, 'rb') as cert_file:
                    certificate_content = cert_file.read()
                    certificate_base64 = base64.b64encode(certificate_content).decode()

               # Leer y codificar el archivo .key
               with open(private_key_path, 'rb') as key_file:
                    private_key_content = key_file.read()
                    private_key_base64 = base64.b64encode(private_key_content).decode()

               # Imprimir los valores codificados
               print("Certificado en Base64:")
               print(certificate_base64)
               print("Clave Privada en Base64:")
               print(private_key_base64)
               
               csd_data = {
                    "Rfc": rfc,
                    "Certificate": certificate_base64,
                    "Private": private_key_base64,
                    "PrivateKeyPassword": key_password,
               } 
               
               print(csd_data)
               
               # URL de la API de Facturama
               url = "https://apisandbox.facturama.mx/api-lite/csds"
               username = "AranzaInade"
               password = "Puebla4990"
               response = requests.post(url, json=csd_data, auth=(username, password))
               if response.status_code == 201:
                    return redirect('success')
               else:
                    messages.success(request, 'CSD cargado correctamente.')
                    return render(request, 'facturacion/cargar_csd.html', {'form': form, 'error': response.text})
               
                    

               return redirect(cargar_csd)  # Redirige al mismo formulario
     else:
          form = CSDForm()
     return render(request, 'facturacion/cargar_csd.html', {'form': form})

def convertir_a_base64(file):
     
    return base64.b64encode(file.read()).decode('utf-8')

def success(request):
    return render(request, 'success.html', {'message': 'CSD cargado exitosamente.'})
          
          