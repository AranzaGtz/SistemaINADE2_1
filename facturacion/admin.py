from django.contrib import admin

from facturacion.models import CFDI, CSD, Emisor, Receptor

# Register your models here.
# Registrando todos los modelos en el admin
admin.site.register(Emisor)
admin.site.register(Receptor)
admin.site.register(CFDI)
admin.site.register(CSD)