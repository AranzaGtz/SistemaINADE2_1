import re
from django import forms
from accounts.forms import ServicioForm
from accounts.utils import obtener_configuracion
from .models import CSD, Factura
from django.forms import inlineformset_factory, formset_factory
from .models import Factura, Servicio

class SeleccionForm(forms.Form):
    TIPO_OPCIONES = [
        ('cotizacion', 'Cotización'),
        ('orden_trabajo', 'Orden de Trabajo'),
    ]

#    FORMULARIO PARA CARGAR INFORMACIÓN PARA CSD O SELLO DIGITAL
class CSDForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'aria-describedby': 'passwordHelpBlock'}), label="Contraseña del CSD")

    class Meta:
        model = CSD
        # Especifica los campos del formulario
        fields = ['rfc','cer_file', 'key_file', 'password']
        widgets = {
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'cer_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'formCerFile'}),
            'key_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'formKeyFile'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'aria-describedby': 'passwordHelpBlock'}),
        }
        labels = {
            'cer_file': 'Archivo .cer',
            'key_file': 'Archivo .key',
        }



    def clean_cer_file(self):
        cer_file = self.cleaned_data.get('cer_file')

        if cer_file:
            # Verificar si el archivo tiene la extensión .cer
            if not cer_file.name.endswith('.cer'):
                raise forms.ValidationError(
                    'El archivo debe tener la extensión .cer.')

        return cer_file

    def clean_key_file(self):
        key_file = self.cleaned_data.get('key_file')

        if key_file:
            # Verificar si el archivo tiene la extensión .key
            if not key_file.name.endswith('.key'):
                raise forms.ValidationError(
                    'El archivo debe tener la extensión .key.')

        return key_file

#   FORMULARIO DE FACTURAS
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__' 

#    FORMULARIO PARA DATOS DE UNA FACTURAR Encabezado
class FacturaEncabezadoForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['sucursal', 'almacen', 'tipo_moneda','orden_compra', 'uso_cfdi', 'forma_pago','metodo_pago']
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'form-control form-select', 'placeholder': 'Seleccione sucursal', 'id': 'inputGroupSelect03'}),
            'almacen': forms.Select(attrs={'class': 'form-control ', 'placeholder': 'Seleccione almacen'}),
            'tipo_moneda': forms.Select(attrs={'class': 'form-control ', 'placeholder': 'Seleccione tipo moneda'}),
            'orden_compra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID de orden de compra'}),
            'uso_cfdi': forms.Select(attrs={'class': 'form-control'}),
            'forma_pago': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configuracion = obtener_configuracion()
        if configuracion:
            self.fields['tipo_moneda'].initial = configuracion.moneda_predeterminada

#    FORMULARIO PARA DATOS DE UNA FACTURAR Pie
class FacturaPieForm(forms.ModelForm):
    direccion = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'aria-describedby': 'passwordHelpBlock'}),
        label="Dirección Fiscal"
    )
    notificacion = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'fomr-control'}),
        label="Notificación ",
        required=False  # Opcional: Si quieres que sea obligatorio, cambia esto a True o elimina esta línea
    )

    class Meta:
        model = Factura
        fields = ['direccion', 'comentarios', 'notificacion', 'correos']
        widgets = {
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'correos': forms.TextInput(attrs={'class': 'form-control'})
        }
        optional = ['comentarios', 'correos']

#    FORMULARIO PARA DATOS DE UNA FACTURAR Totales
class FacturaTotalesForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control',
                                 'placeholder': 'Ingrese un número decimal', 'inputmode': 'decimal'})
    )
    iva = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control',
                                 'placeholder': 'Ingrese un número decimal', 'inputmode': 'decimal'})
    )

    class Meta:
        model = Factura
        fields = ['subtotal', 'iva', 'tasa_iva', 'total']
        widgets = {
            'total': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'form-control',
                'placeholder': 'Ingrese un número decimal',
                'inputmode': 'decimal',  # Este atributo sugiere la entrada de números sin flechas
            }),
            'tasa_iva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la tasa de IVA'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configuracion = obtener_configuracion()
        if configuracion:
            self.fields['tasa_iva'].initial = configuracion.tasa_iva_default


#   FORMULARIO SET PARA SERVIVIO
ServicioFormset = formset_factory(
    ServicioForm,
    extra=1,
    can_delete=True
)
