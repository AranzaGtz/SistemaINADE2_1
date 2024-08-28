# Create your models here.
from django.db import models
from accounts.models import Cotizacion


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
    emisor = models.ForeignKey(Emisor, on_delete=models.CASCADE)
    receptor = models.ForeignKey(Receptor, on_delete=models.CASCADE)
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
    
    def __str__(self):
        return f"Factura {self.uuid} para Cotización {self.cotizacion.id_personalizado}"
