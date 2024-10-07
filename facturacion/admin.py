from django.contrib import admin

from facturacion.models import CSD, Comprobante, Factura

# Register your models here.
# Registrando todos los modelos en el admin
admin.site.register(CSD)
admin.site.register(Factura)
admin.site.register(Comprobante)