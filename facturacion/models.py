# Create your models here.
from django.db import models
from accounts.models import Almacen, Cotizacion, Organizacion, Servicio, Sucursal


class CFDI(models.Model):
    uuid = models.CharField(max_length=36, unique=True)
    emisor = models.CharField(max_length=255, null=True, blank=True)
    receptor = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    sello_cfd = models.TextField()
    sello_sat = models.TextField()
    no_certificado_cfd = models.CharField(max_length=20)
    no_certificado_sat = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)

    # Campos para almacenar documentos
    xml_file = models.FileField(upload_to='cfdis/xml/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='cfdis/pdf/', null=True, blank=True)

    def __str__(self):
        return f"CFDI {self.uuid}"


class CSD(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, blank=True, null=True)  # Relación con Organización
    rfc = models.CharField(max_length=13, unique=True)#Aqui Organizacion.rfc sea guardado automaticamente
    cer_file = models.FileField(upload_to='csds/cer/')
    key_file = models.FileField(upload_to='csds/key/')
    password = models.CharField(max_length=255)

class Factura(models.Model):
    cotizacion = models.OneToOneField(Cotizacion, on_delete=models.PROTECT,blank=True, null=True)
    uuid = models.CharField(max_length=50, unique=True)  # UUID del CFDI
    xml_timbrado = models.FileField(upload_to='facturas_xmls/', null=True, blank=True)
    pdf_factura = models.FileField(upload_to='facturas_pdfs/', null=True, blank=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=False)  # True para "Pagada", False para "Pendiente"
    # Nuevos campos
    metodo_pago = models.CharField(max_length=5,choices=[('PUE', 'Pago en una sola exhibición'), ('PPD', 'Pago en parcialidades o diferido')] , default='PUE')
    forma_pago = models.CharField(max_length=5,choices=[('01', 'Efectivo'), ('03', 'Transferencia electrónica de fondos'),('99','Por definir')] , default='99')
    uso_cfdi = models.CharField(max_length=5, choices=[('G01', 'Adquisición de mercancias'), ('G03', 'Gastos en general')], default='G03')
    rfc_receptor = models.CharField(max_length=13)
    regimen_fiscal_receptor = models.CharField(max_length=3)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    orden_compra = models.CharField(max_length=255, blank=True, null=True)
    comentarios = models.CharField(blank=True, null=True, max_length=255)
    tm = [
        ('MXN', 'MXN - Moneda Nacional Mexicana'),
        ('USD', 'USD - Dolar Estadunidense')
    ]
    tipo_moneda = models.CharField(max_length=100, choices=tm)
    opciones_iva = [
        ('0.08', '8%'),
        ('0.16', '16%')
    ]
    tasa_iva = models.CharField(max_length=4, choices=opciones_iva)
    correos = models.CharField(max_length=255, blank= True, null=True)
    
    def __str__(self):
        if self.cotizacion and self.cotizacion.id_personalizado:
            return f"Factura {self.uuid} para Cotización {self.cotizacion.id_personalizado}"
        return f"Factura {self.uuid}"