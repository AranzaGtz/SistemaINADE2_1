import re
from django import forms
from accounts.forms import ServicioForm
from accounts.utils import obtener_configuracion
from .models import CSD, Factura
from django.forms import  formset_factory
from .models import Factura
from datetime import datetime, timedelta, timezone

MOTIVOS = [
    ('01','01 - Comprovante emitido con errores con relación.'),
    ('02','02 - Comprovante emitido con errores sin relación.'),
    ('03','03 - No se llevó a cabo la operación.'),
    ('04','04 - Operación nominativa relacionada en una global.')
]

METODOS_PAGO_CHOICES = [
    ("01", "01 - Efectivo"),
    ("02", "02 - Cheque nominativo"),
    ("03", "03 - Transferencia electrónica de fondos"),
    # ("04", "04 - Tarjeta de crédito"),
    # ("05", "05 - Monedero electrónico"),
    # ("06", "06 - Dinero electrónico"),
    # ("08", "08 - Vales de despensa"),
    # ("12", "12 - Dación en pago"),
    # ("13", "13 - Pago por subrogación"),
    # ("14", "14 - Pago por consignación"),
    # ("15", "15 - Condonación"),
    # ("17", "17 - Compensación"),
    # ("23", "23 - Novación"),
    # ("24", "24 - Confusión"),
    # ("25", "25 - Remisión de deuda"),
    # ("26", "26 - Prescripción o caducidad"),
    # ("27", "27 - A satisfacción del acreedor"),
    # ("28", "28 - Tarjeta de débito"),
    # ("29", "29 - Tarjeta de servicios"),
    # ("30", "30 - Aplicación de anticipos"),
    # ("31", "31 - Intermediarios"),
    ("99", "99 - Por definir"),
]

#   FORMULARIO PARA GENERAR COMPROBANTE DE PAGO
class ComprobantePagoForm(forms.Form):
    Date = forms.DateTimeField(label='Fecha de Pago',widget=forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-control', 'id': 'Date'}), required=False)
    PaymentForm = forms.ChoiceField(choices=METODOS_PAGO_CHOICES, label='Método de pago', widget=forms.Select(attrs={'class':'form-select', 'id': 'PaymentForm'}), required=False)
    Amount = forms.DecimalField(label='Monto', widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'Amount'}), required=False)
    OperationNumber = forms.CharField(label='Referencia', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'OperationNumber'}), required=False)
    ForeignAccountNamePayer = forms.CharField(label='Nombre de la cuenta del pagador', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'ForeignAccountNamePayer'}), required=False)
    PayerAccount = forms.CharField(label='Cuenta del pagador', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'PayerAccount'}), required=False)
    RfcReceiverBeneficiaryAccount = forms.CharField(label='RFC del beneficiario de la cuenta', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'RfcReceiverBeneficiaryAccount'}), required=False)
    BeneficiaryAccount = forms.CharField(label='Cuenta del beneficiario', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'BeneficiaryAccount'}), required=False)

#   FORMULARIO PARA CANCELAR FACTURA
class CancelarCFDI(forms.Form):

    motive = forms.ChoiceField(choices=MOTIVOS, label='Selecciona el motivo por la que se realizara la cancelación.', widget=forms.Select(attrs={'class':'form-select', 'id': 'select_opciones'}))
    uuid_replacement = forms.CharField(required=False, label='UUID que va a remplazar', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'uuid_replacement'}))
    factura_id = forms.CharField(required=True,widget=forms.HiddenInput())

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
        fields = ['tipo_moneda','OrderNumber', 'uso_cfdi', 'forma_pago','metodo_pago']
        widgets = {
            'tipo_moneda': forms.Select(attrs={'class': 'form-control ', 'placeholder': 'Seleccione tipo moneda'}),
            'OrderNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID de orden de compra'}),
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
