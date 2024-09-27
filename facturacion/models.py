# Create your models here.
from django.db import models
from accounts.models import   OrdenTrabajo, Organizacion, Persona
from django.utils import timezone

class CSD(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, blank=True, null=True)  # Relación con Organización
    rfc = models.CharField(max_length=13, unique=True)#Aqui Organizacion.rfc sea guardado automaticamente
    cer_file = models.FileField(upload_to='csds/cer/')
    key_file = models.FileField(upload_to='csds/key/')
    password = models.CharField(max_length=255)


class Factura(models.Model):
    
    # ID interno de la factura en tu sistema
    id = models.CharField(max_length=4, unique=True, blank=True,primary_key=True)
    
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
    uso_cfdi = models.CharField(max_length=5, choices=[('G01', 'Adquisición de mercancias'), ('G03', 'Gastos en general')], default='G03')
    forma_pago = models.CharField(max_length=5,choices=[('01', 'Efectivo'), ('03', 'Transferencia electrónica de fondos'),('99','Por definir')] , default='99')
    metodo_pago = models.CharField(max_length=5,choices=[('PUE', 'Pago en una sola exhibición'), ('PPD', 'Pago en parcialidades o diferido')] , default='PUE')
    
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
    
    
    def formatted_id(self):
        # Formatea el ID para que tenga siempre cuatro dígitos con ceros a la izquierda
        return f'{self.id:04}'
    
    def __str__(self):
        # Utiliza el método formatted_id para mostrar la factura con el ID formateado
        return f'Factura {self.formatted_id()}'