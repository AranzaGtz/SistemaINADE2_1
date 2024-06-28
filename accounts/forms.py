from django import forms
from .models import Concepto, CustomUser, Formato, Metodo,Persona,Prospecto, Cliente, Empresa, Direccion, InformacionContacto, Servicio, Cotizacion
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

#   FORMULARIO PARA CREAR USUARIO
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'celular', 'rol')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre de usuario',  
                'required': 'True'
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'required': 'False'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos', 'required': 'False'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico', 'required': 'True'}),
            'celular': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Celular', 'required': 'False'}),
            'rol': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona Tipo de Rol', 'required': 'True'}),
        }
        
#   FORMULARIO PARA CAMBIAR USUARIO
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'celular', 'rol')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'required': 'False'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos', 'required': 'False'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico', 'required': 'True'}),
            'celular': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Celular', 'required': 'False'}),
            'rol': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona Tipo de Rol', 'required': 'True'}),
        }
      
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
            'titulo': forms.Select(attrs={'class':'form-control','placeholder':'Selecciona un titulo','required':'False'}),
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
        fields = ['metodo']
        widgets = {
            'metodo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del método'}),
        }

#   FORMULARIO PARA SERVICIO
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['metodo','nombre_servicio', 'descripcion', 'precio_sugerido' ]
        widgets = {
            'metodo': forms.Select(attrs={'class': 'form-control'}),
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio o concepto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio o concepto','rows': 2}),
            'precio_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio sugerido'}),
        }

#   FORMULARIO PARA CONCEPTO
class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = ['servicio','cantidad_servicios', 'precio',  'notas']
        widgets = {
            'servicio': forms.Select(attrs={'class':'form-control'}),
            'cantidad_servicios': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio sugerido'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas adicionales','rows': 3}),
        }

ConceptoFormSet = inlineformset_factory(Cotizacion, Concepto, form=ConceptoForm, extra=1, can_delete=True)
ConceptoChangeFormSet = inlineformset_factory(Cotizacion, Concepto, form=ConceptoForm, extra=0, can_delete=True)

#   FORMULARIO PARA COTIZACION
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['fecha_solicitud', 'fecha_caducidad', 'metodo_pago', 'tasa_iva', 'notas', 'correos_adicionales', 'persona']
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_caducidad': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'metodo_pago': forms.Select(attrs={'class':'form-control','placeholder':'Selecciona Tipo de Moneda','required':'True'}),
            'tasa_iva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la tasa de IVA'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas que aparecerán al final de la cotización (Opcional).','rows': 3}),
            'correos_adicionales': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingresa correos adicionales, separados por comas (Opcional)','rows': 3}),
            'persona': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona el cliente'}),
        }
        
#   FORMULARIO PARA CAMBIAR COTIZACION
class CotizacionChangeForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['fecha_solicitud', 'fecha_caducidad', 'metodo_pago', 'tasa_iva', 'notas', 'correos_adicionales', 'persona']
        widgets = {
            'fecha_solicitud': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Fecha en formato dd-mm-aaaa'}),
            'fecha_caducidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Fecha en formato dd-mm-aaaa'}),
            'metodo_pago': forms.Select(attrs={'class':'form-control','placeholder':'Selecciona Tipo de Moneda','required':'True'}),
            'tasa_iva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la tasa de IVA'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas que aparecerán al final de la cotización (Opcional).','rows': 3}),
            'correos_adicionales': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingresa correos adicionales, separados por comas (Opcional)','rows': 3}),
            'persona': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona el cliente'}),
        }
        
class TerminosForm(forms.ModelForm):
    class Meta:
        model = Formato
        fields = ['terminos', 'avisos']
        widgets = {
            'terminos': forms.Textarea(attrs={'class': 'form-control'}),
            'avisos': forms.Textarea(attrs={'class': 'form-control'}),
        }