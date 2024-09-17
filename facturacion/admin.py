from django.contrib import admin

from facturacion.models import CFDI, CSD

# Register your models here.
# Registrando todos los modelos en el admin
admin.site.register(CFDI)
admin.site.register(CSD)