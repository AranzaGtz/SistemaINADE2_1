# Create your models here.
from django.db import models
from accounts.models import   OrdenTrabajo, Organizacion, Persona
from django.utils import timezone

METODOS_PAGO_CHOICES = [
    ("01", "Efectivo"),
    ("02", "Cheque nominativo"),
    ("03", "Transferencia electrónica de fondos"),
    ("04", "Tarjeta de crédito"),
    ("05", "Monedero electrónico"),
    ("06", "Dinero electrónico"),
    ("08", "Vales de despensa"),
    ("12", "Dación en pago"),
    ("13", "Pago por subrogación"),
    ("14", "Pago por consignación"),
    ("15", "Condonación"),
    ("17", "Compensación"),
    ("23", "Novación"),
    ("24", "Confusión"),
    ("25", "Remisión de deuda"),
    ("26", "Prescripción o caducidad"),
    ("27", "A satisfacción del acreedor"),
    ("28", "Tarjeta de débito"),
    ("29", "Tarjeta de servicios"),
    ("30", "Aplicación de anticipos"),
    ("31", "Intermediarios"),
    ("99", "Por definir"),
]
    
PAYMENT_METHOD_CHOICES = [
    ('PPD', 'Pago en parcialidades ó diferido'),
    ('PUE', 'Pago en una sola exhibición'),
]

CFDIUSES = [
    ("CN01", "Nómina"),
    ("CP01", "Pagos"),
    ("D01", "Honorarios médicos, dentales y gastos hospitalarios."),
    ("D02", "Gastos médicos por incapacidad o discapacidad"),
    ("D03", "Gastos funerales."),
    ("D04", "Donativos."),
    ("D05", "Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)."),
    ("D06", "Aportaciones voluntarias al SAR."),
    ("D07", "Primas por seguros de gastos médicos."),
    ("D08", "Gastos de transportación escolar obligatoria."),
    ("D09", "Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones."),
    ("D10", "Pagos por servicios educativos (colegiaturas)"),
    ("G01", "Adquisición de mercancias"),
    ("G02", "Devoluciones, descuentos o bonificaciones"),
    ("G03", "Gastos en general"),
    ("I01", "Construcciones"),
    ("I02", "Mobilario y equipo de oficina por inversiones"),
    ("I03", "Equipo de transporte"),
    ("I04", "Equipo de computo y accesorios"),
    ("I05", "Dados, troqueles, moldes, matrices y herramental"),
    ("I06", "Comunicaciones telefónicas"),
    ("I07", "Comunicaciones satelitales"),
    ("I08", "Otra maquinaria y equipo"),
    ("P01", "Por Definir"),
    ("S01", "Sin efectos fiscales"),
]
    
class CSD(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, blank=True, null=True)  # Relación con Organización
    rfc = models.CharField(max_length=13, unique=True)#Aqui Organizacion.rfc sea guardado automaticamente
    cer_file = models.FileField(upload_to='csds/cer/')
    key_file = models.FileField(upload_to='csds/key/')
    password = models.CharField(max_length=255)

class Factura(models.Model):
    

    # ID interno de la factura en tu sistema
    id = models.AutoField(primary_key=True,max_length=4, unique=True) # Folio
    
    # ID devuelto por la API de Facturama 
    cfdi_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # Campos relacionados con la orden de trabajo y datos fiscales
    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT, blank=True, null=True,default=0)
    cliente = models.ForeignKey(Persona, on_delete=models.PROTECT,default=0) # Relación con el cliente
    emisor = models.ForeignKey(Organizacion, on_delete=models.PROTECT,default=0) # Relación con el emisor
    
    # Información de pago y moneda
    tm = [
        ('MXN', 'MXN - Moneda Nacional Mexicana'),
        ('USD', 'USD - Dolar Estadunidense')
    ]
    tipo_moneda = models.CharField(max_length=100, choices=tm)
    uso_cfdi = models.CharField(max_length=5, choices=CFDIUSES, default='G03')
    forma_pago = models.CharField(max_length=5,choices=METODOS_PAGO_CHOICES , default='99')
    metodo_pago = models.CharField(max_length=5,choices=PAYMENT_METHOD_CHOICES , default='PUE')
    
    # Información de los totales de la factura
    ExchangeRate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    Discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    opciones_iva = [
        ('0.08', '8%'),
        ('0.16', '16%')
    ]
    tasa_iva = models.CharField(max_length=4, choices=opciones_iva)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Fecha y hora de creación de la factura
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    # Estado de la factura (ej. timbrada, cancelada, etc.)
    estado = models.CharField(max_length=20, default='Creada')

    # Campos para almacenar documentos
    xml_file = models.FileField(upload_to='cfdis/xml/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='cfdis/pdf/', null=True, blank=True)
    
    # Información adicional de la factura
    ExpeditionPlace = models.CharField(max_length=5, blank=True, null=True)
    cfdi_type = models.CharField(max_length=20, blank=True, null=True)
    Type = models.CharField(max_length=20, blank=True, null=True)
    OrderNumber = models.CharField(max_length=20, blank=True, null=True)
    comentarios = models.CharField(blank=True, null=True, max_length=255)
    correos = models.CharField(max_length=255, blank= True, null=True)
    
    #   Cadena Original del Complemento de Certificación Digital del SAT
    OriginalString = models.TextField(blank= True, null=True)
    #   Sello Digital del CFDI
    CfdiSign = models.TextField(blank= True, null=True)
    #   Sello Digital del SAT
    SatSign = models.TextField(blank= True, null=True)
    
    def generate_new_id(self, formato):
        last_cotizacion = Factura.objects.order_by('id').last()
        new_id = '0001' if not last_cotizacion else str(int(last_cotizacion.id_personalizado) + 1).zfill(4)
        
        return formato.format(seq=new_id)
    
    def save(self, *args, **kwargs):
        factura = Factura.objects.first()
        
        if factura:
            if not self.id:
                self.id = self.generate_new_id()
    
    def __str__(self):
        # Utiliza el método formatted_id para mostrar la factura con el ID formateado
        return f'Factura {self.formatted_id()}'