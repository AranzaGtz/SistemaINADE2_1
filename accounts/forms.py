from django import forms
from .models import CustomUser, Metodo,Persona,Prospecto, Cliente, Empresa, Direccion, InformacionContacto, Servicio
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        
        model = CustomUser
        
        fields = ('username', 'first_name', 'last_name', 'email', 'celular', 'rol')
        
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'celular', 'rol')
      
class InformacionContactoForm(forms.ModelForm):
    class Meta:
        model = InformacionContacto
        fields = ['correo_electronico', 'telefono', 'celular', 'fax']
          
class PersonaForm (forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'titulo', 'informacion_contacto', 'empresa']
        
class ProspectoForm(PersonaForm):
    class Meta(PersonaForm.Meta):
        model = Prospecto
        fields = ['nombre', 'apellidos', 'titulo']

class ClienteForm(PersonaForm):
    class Meta(PersonaForm.Meta):
        model = Cliente
    
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle','numero', 'colonia', 'ciudad', 'codigo', 'estado']
        
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre_empresa', 'rfc', 'moneda', 'condiciones_pago']

class MetodoForm(forms.ModelForm):
    class Meta:
        model = Metodo
        fields = ['nombre', 'leyenda']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del método'}),
            'leyenda': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leyenda descriptiva del método'}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['servicio', 'descripcion', 'precio_sugerido']
        widgets = {
            'servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio o concepto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio o concepto'}),
            'precio_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio sugerido'}),
        }
