# Create your models here.
from django.db import models
from accounts.models import Almacen, Cotizacion, Servicio, Sucursal


class Emisor(models.Model):
    rfc = models.CharField(max_length=13, unique=True)
    nombre = models.CharField(max_length=255)
    regimen_fiscal = models.CharField(max_length=3)

    def __str__(self):
        return self.nombre


class Receptor(models.Model):
    rfc = models.CharField(max_length=13)
    nombre = models.CharField(max_length=255)
    uso_cfdi = models.CharField(max_length=3)

    def __str__(self):
        return self.nombre


class CFDI(models.Model):
    uuid = models.CharField(max_length=36, unique=True)
    emisor = models.ForeignKey(Emisor, on_delete=models.PROTECT)
    receptor = models.ForeignKey(Receptor, on_delete=models.PROTECT)
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
    rfc = models.CharField(max_length=13, unique=True)
    cer_file = models.FileField(upload_to='csds/cer/')
    key_file = models.FileField(upload_to='csds/key/')
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.rfc


class Factura(models.Model):
    cotizacion = models.OneToOneField(Cotizacion, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=50, unique=True)  # UUID del CFDI
    xml_timbrado = models.FileField(upload_to='facturas_xmls/', null=True, blank=True)
    pdf_factura = models.FileField(upload_to='facturas_pdfs/', null=True, blank=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=False)  # True para "Pagada", False para "Pendiente"
    # Nuevos campos
    metodo_pago = models.CharField(max_length=5, choices=[('01', 'Efectivo'), ('03', 'Transferencia electrónica de fondos')], default='03')
    forma_pago = models.CharField(max_length=5, choices=[('PUE', 'Pago en una sola exhibición'), ('PPD', 'Pago en parcialidades o diferido')], default='PUE')
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
        return f"Factura {self.uuid} para Cotización {self.cotizacion.id_personalizado}"

class ConceptoFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='conceptos', on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)  # Nombre del servicio
    cantidad_servicios = models.IntegerField()  # Cantidad de servicios
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario
    importe = models.DecimalField(max_digits=10, decimal_places=2)  # Importe total del concepto
    
    def __str__(self):
        return f'{self.servicio} - {self.cantidad_servicios} x {self.precio}'

    def calcular_importe(self):
        return self.cantidad_servicios * self.precio

    def save(self, *args, **kwargs):
        self.importe = self.calcular_importe()
        super().save(*args, **kwargs)