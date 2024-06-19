from django import forms
from .models import Concepto, CustomUser, Metodo,Persona,Prospecto, Cliente, Empresa, Direccion, InformacionContacto, Servicio, Cotizacion
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        
        model = CustomUser
        
        fields = ('username', 'first_name', 'last_name', 'email', 'celular', 'rol')
        
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'celular', 'rol')
      
#   FORMULARIO PARA INFROMACION DE CONTACTO
class InformacionContactoForm(forms.ModelForm):
    class Meta:
        model = InformacionContacto
        fields = ['correo_electronico', 'telefono', 'celular', 'fax']
        widgets = {
            'correo_electronico': forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo electronico','required':'True'}),
            'telefono': forms.NumberInput(attrs={'class':'form-control','placeholder':'Telefono','required':'False','pattern':"[0-9]{10}"}),
            'celular': forms.NumberInput(attrs={'class':'form-control','placeholder':'Celular','required':'True'}),
            'fax': forms.NumberInput(attrs={'class':'form-control','placeholder':'Fax'}),
        }
 
#   FORMULARIO PARA PERSONA         
class PersonaForm (forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'titulo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Nombre del método','required':'True'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Ambos apellidos','required':'True'}),
            'titulo': forms.Select(attrs={'class':'form-control','placeholder':'Selecciona un titulo','required':'True'}),
        }

#   FORMULARIO PARA PROSPECTO        
class ProspectoForm(forms.ModelForm):
    class Meta:
        model = Prospecto
        fields = ['persona']
        widgets = {
            'persona': forms.Select(attrs={'class': 'form-control'}),
        }

#   FORMULARIO PARA CLIENTE  
class ClienteForm(forms.ModelForm):
    class Meta :
        model = Cliente
        fields = ['persona']

#   FORMULARIO PARA DIRECCION DE EMPRESA
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle','numero', 'colonia', 'ciudad', 'codigo', 'estado']
        widgets = {
            'calle':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Calle','required':'True'}),
            'numero':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Número exterior','required':'True','pattern':r"[0-9A-Za-z\s\-]+"}),
            'colonia':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Colonia','required':'True'}),
            'ciudad':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Ciudad','required':'True'}),
            'codigo':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Código Postal','required':'True','pattern':r"[0-9]{5}"}),
            'estado':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Estado','required':'True'}),
        }
      
#   FORMULARIO PARA EMPRESA  
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre_empresa', 'rfc', 'moneda', 'condiciones_pago']
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa el Nombre de la Empresa','required':'True'}),
            'rfc': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa RFC','required':'False','pattern':r"[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}"}),
            'moneda': forms.Select(attrs={'class':'form-control','placeholder':'Selecciona Tipo de Moneda','required':'True'}),
            'condiciones_pago': forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingresa los días en cada cuanto se pagara.'}),
        }

#   FORMULARIO PARA METODO
class MetodoForm(forms.ModelForm):
    class Meta:
        model = Metodo
        fields = ['nombre', 'leyenda']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del método'}),
            'leyenda': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leyenda descriptiva del método'}),
        }

#   FORMULARIO PARA SERVICIO
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['servicio', 'descripcion', 'precio_sugerido']
        widgets = {
            'servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio o concepto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio o concepto'}),
            'precio_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio sugerido'}),
        }

#   FORMULARIO PARA CONCEPTO
class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = ['nombre_concepto', 'cantidad_servicios', 'notas']
        widgets = {
            'nombre_concepto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_servicios': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas adicionales'}),
        }

#   FORMULARIO PARA COTIZACION
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['fecha_solicitada', 'fecha_caducidad', 'metodo_pago', 'tasa_iva', 'notas', 'correoss_adicionales']
        widgets = {
            'fecha_solicitada': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa fecha de solicitud'}),
            'fecha_caducidad': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa fecha de caducidad'}),
            'metodo_pago': forms.Select(attrs={'class':'form-control','placeholder':'Selecciona Tipo de Moneda','required':'True'}),
            'tasa_iva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la tasa de IVA'}),
            'Notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingresa tus notas aquí.'}),
            'correos_adicionales': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingresa correos adicionales, separados por comas'}),
        }