from django import forms
from .models import Concepto, CustomUser, FormatoCotizacion, FormatoOrden, Metodo, OrdenTrabajo, Organizacion, Persona, Prospecto, Empresa, Direccion, InformacionContacto, Queja, Servicio, Cotizacion, Titulo
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

# ---      USUARIOS     ---
#   FORMULARIO PARA CREAR USUARIO
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',
                  'email', 'celular', 'rol')
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

#----------------------------------------------------
# MODELO PARA CLIENTES
#----------------------------------------------------

#   FORMULARIO PARA DIRECCION DE EMPRESA
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'numero', 'colonia', 'ciudad', 'codigo', 'estado']
        widgets = {
            'calle':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Calle', 'required': 'True'}),
            'numero':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Número exterior', 'required': 'True', 'pattern': r"[0-9A-Za-z\s\-]+"}),
            'colonia':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Colonia', 'required': 'True'}),
            'ciudad':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Ciudad', 'required': 'True'}),
            'codigo':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Código Postal', 'required': 'True', 'pattern': r"[0-9]{5}"}),
            'estado':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Estado', 'required': 'True'}),
        }

#   FORMULARIO PARA EMPRESA
class EmpresaForm(forms.ModelForm):
    # Campos de Direccion
    calle =     forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle'}))
    numero =    forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}))
    colonia =   forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Colonia'}))
    ciudad =    forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}))
    codigo =    forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}))
    estado =    forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}))

    class Meta:
        model = Empresa
        fields = ['nombre_empresa', 'rfc', 'moneda', 'condiciones_pago',
                  'calle', 'numero', 'colonia', 'ciudad', 'codigo', 'estado']
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el Nombre de la Empresa ', 'required': 'True'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa RFC ', 'required': 'False', 'pattern': r"[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}"}),
            'moneda': forms.Select(attrs={'class': 'form-control'}),
            'condiciones_pago': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Días de pago '}),
        }

# ---      CLIENTES     ---

#   FORMULARIO PARA INFROMACION DE CONTACTO
class InformacionContactoForm(forms.ModelForm):
    class Meta:
        model = InformacionContacto
        fields = ['correo_electronico', 'telefono', 'celular', 'fax']
        widgets = {
            'correo_electronico':   forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electronico', 'required': 'True'}),
            'telefono':             forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Telefono', 'required': 'False', 'pattern': "[0-9]{10}"}),
            'celular':              forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Celular', 'required': 'True'}),
            'fax':                  forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fax','required': 'False'}),
        }
        optional = ['telefono', 'fax']

class TituloForm(forms.ModelForm):
    class Meta:
        model = Titulo
        fields = ['abreviatura','titulo']
        widgets = {
            'abreviatura': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Abreviatura'}),
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo'})
        }

#   FORMULARIO PARA PERSONA
class PersonaForm(forms.ModelForm):
    titulo = forms.ModelChoiceField(
        queryset=Titulo.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Campos de InformacionContactoForm
    correo_electronico = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    telefono = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'})
    )
    celular = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'})
    )
    fax = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fax'})
    )

    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'titulo', 'correo_electronico', 'telefono', 'celular', 'fax']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Nombre del cliente', 'required': 'True'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Ambos apellidos del cliente', 'required': 'True'}),
            'titulo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona un título', 'required': 'False'}),
        }
    optional = ['telefono', 'fax', 'titulo']

#   FORMULARIO PARA PROSPECTO
class ProspectoForm(forms.ModelForm):
    class Meta:
        model = Prospecto
        fields = ['persona']
        widgets = {
            'persona': forms.Select(attrs={'class': 'form-control'}),
        }

# ---      METODOS Y SERVICIOS     ---

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
        fields = ['nombre_servicio', 'descripcion',
                  'precio_sugerido']
        widgets = {

            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio o concepto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio o concepto', 'rows': 2}),
            'precio_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio sugerido'}),

        }

#   FORMULARIO PARA SERVICIO
class ServicioForm2(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['metodo', 'nombre_servicio', 'precio_sugerido', 'descripcion']
        widgets = {
            'metodo': forms.Select(attrs={'class': 'form-control'}),
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio'}),
            'precio_sugerido': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio sugerido'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio'}),
        }

#   FORMULARIO PARA CONCEPTO
class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = ['servicio', 'cantidad_servicios', 'precio',  'notas']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-control', 'list': 'servicios-list', 'autocomplete': 'off'}),
            'cantidad_servicios': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio sugerido'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas adicionales', 'rows': 3}),
        }

ConceptoFormSet = inlineformset_factory(
    Cotizacion, Concepto, form=ConceptoForm, extra=1, can_delete=True)

# ---      COTIZACIONES     ---

#   FORMULARIO PARA COTIZACION
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['fecha_solicitud', 'fecha_caducidad', 'metodo_pago','tasa_iva', 'notas', 'correos_adicionales']
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_caducidad': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona Tipo de Moneda', 'required': 'True'}),
            'tasa_iva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la tasa de IVA'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas que aparecerán al final de la cotización (Opcional).', 'rows': 3}),
            'correos_adicionales': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingresa correos adicionales, separados por comas (Opcional)', 'rows': 3}),
        }


#   FORMULARIO PARA CAMBIAR COTIZACION
class CotizacionChangeForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['metodo_pago', 'tasa_iva', 'notas', 'correos_adicionales']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona Tipo de Moneda', 'required': 'True'}),
            'tasa_iva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la tasa de IVA'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notas que aparecerán al final de la cotización (Opcional).', 'rows': 3}),
            'correos_adicionales': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingresa correos adicionales, separados por comas (Opcional)', 'rows': 3}),
        }

# ---      ORGANIZACIÓN     ---

#   FORMULARIO PARA LA ORGANIZACION
class OrganizacionForm(forms.ModelForm):
    class Meta:
        model = Organizacion
        fields = ['nombre', 'direccion', 'telefono', 'pagina_web']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'pagina_web': forms.URLInput(attrs={'class': 'form-control'}),
        }

#   FORMULARIO PARA QUE USUARIO SUBA ORDEN DE TRABAJO
class OrdenPedidoForm(forms.Form):
    archivo = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'custom-file-input','id': 'archivo', 'onchange': 'actualizarNombreArchivo(this)'}),label='')

#   FORMULARIO PARA ORDEN DE TRABAJO
class OrdenTrabajoForm(forms.ModelForm):
    # Campos adicionales del cliente
    class Meta:
        model = OrdenTrabajo
        fields = ['receptor','gestion']
        widgets = {
            'receptor': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'receptor': 'Seleccione el receptor de la orden:',
        }

#   FORMULARIO PARA FORMATOS DE COTIZACIÓN
class FormatoCotizacionForm(forms.ModelForm):
    class Meta:
        model = FormatoCotizacion
        fields = ['nombre_formato','version','emision','terminos','avisos']
        widgets = {
            'nombre_formato': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'emision': forms.DateInput(attrs={'class': 'form-control'}),
            'terminos': forms.Textarea(attrs={'class': 'form-control'}),
            'avisos': forms.Textarea(attrs={'class': 'form-control'}),
        }

#   FORMULARIO PARA FORMATOS DE ORDEN DE TRABAJO
class FormatoOrdenForm(forms.ModelForm):
    class Meta:
        model = FormatoOrden
        fields = ['nombre_formato', 'version', 'emision']
        widgets = {
            'nombre_formato': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'emision': forms.DateInput(attrs={'class': 'form-control'}),
        }

#   FORMULARIO PARA QUEJAS
class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class':'form-control'}),
        }
